from django.test import TestCase, Client
from foodies.account.forms import RegistrationForm
from foodies.account.models import UserProfile
from django.core.urlresolvers import reverse


class RegistrationViewTests(TestCase):

    #makes sure that the register view renders a page with the right
    #template and form used
    def test_registration_view_renders(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.failUnless(isinstance(response.context['form'], RegistrationForm))

    #tests registration with valid data (all fields present)
    def test_registration_view_success(self):
        numUsersBefore = UserProfile.objects.count()
        response = self.client.post(reverse('register'),
                                    data={'firstname': 'Frank',
                                          'lastname': 'McGee',
                                          'email': 'frank@mcgee.com',
                                          'password1': 'qweqwe',
                                          'password2': 'qweqwe'})
        self.assertRedirects(response, '/')
        self.assertEqual(UserProfile.objects.count() - numUsersBefore, 1)
        newUser = UserProfile.objects.latest('user')
        self.assertEqual(newUser.user.first_name, 'Frank')
        self.assertEqual(newUser.user.last_name, 'McGee')
        self.assertEqual(newUser.user.email, 'frank@mcgee.com')

    #test with invalid data
    def test_registration_view_failure(self):
        numUsersBefore = UserProfile.objects.count()
        response = self.client.post(reverse('register'),
                                    data={'firstname': 'Frank',
                                          'lastname': 'McGee',
                                          'email': 'frank@mcgee.com',
                                          'password1': 'qweqwe',
                                          'password2': 'asdasd'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"You must type the same password each time")
        self.assertEqual(numUsersBefore, UserProfile.objects.count())
        

class UpdateProfileTests(TestCase):
    def setUp(self):
        self.c = Client()
        response = self.c.post(reverse('register'),
                                    data={'firstname': 'Test',
                                          'lastname': 'User',
                                          'email': 'Test@User.com',
                                          'password1': '1234',
                                          'password2': '1234'}, follow=True)
        self.newUser = UserProfile.objects.latest('user')
        self.failUnlessEqual(response.status_code, 200)
        
    def test_change_username(self):
        self.c.post(reverse('login'),
                {   'email': 'Test@User.com',
                    'password': '1234'}, follow=True)
        response = self.c.post(reverse('updateUser'),
                {'firstname': 'Altered',
                 'lastname': 'Test',
                 'userPassword': '1234'}, follow=True)
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(self.newUser.user.first_name, 'Altered')
        self.assertEqual(self.newUser.user.last_name, 'Test')
        
       
    def test_change_password(self):
        response = self.c.post(reverse('updateUser'),
                {   'password1': '4321',
                    'password2': '4321',
                    'userPassword': '1234'}, follow=True)
        self.failUnlessEqual(response.status_code, 200)
        username = self.newUser.user.username
        self.c.logout()
        self.failUnlessEqual(self.c.login(username=username, password='4321'), True)

    def test_password_failure(self):
        response = self.c.post(reverse('updateUser'),
                                    data={'firstname': 'Frank',
                                          'userPassword': '1235'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u'Password incorrect, try again')


    def test_change_password_failure(self):
        response = self.c.post(reverse('updateUser'),
                data={  'password1': 4321,
                        'password2': 5321,
                        'userPassword': '1234'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u'You must type the same password each time')


    def test_delete_account(self):
        amountUsers = UserProfile.objects.count()
        response = self.c.get(reverse('delete_user'), follow=True)
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(amountUsers-1, UserProfile.objects.count())













