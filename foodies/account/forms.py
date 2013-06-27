from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import random
import string

attrs_dict = { 'class': 'required' }

class EmailAuthenticationForm(forms.Form):
    """
    Authentication form based off django.contrib.auth.forms.AuthenticationForm.

    This variation relies on email instead of a username.
    """
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields are case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            # ONLY ONE EMAIL PER USER. ELSE THROWS EXCEPTION.

            try:
                username = User.objects.get(email=email).username
                self.user_cache = authenticate(username=username,
                                               password=password)
            except:
                self.user_cache = None
   
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class updateUserForm(forms.Form):
    firstname = forms.CharField(required=False, widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=30)),
                                label=_(u'New First Name'))
    
    lastname = forms.CharField(required=False, widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=30)),
                               label=_(u'New Last Name'))

    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'New Password'))

    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'Confirm New Password'))

    userPassword = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                   label=_(u'Current Password'))

    user = None
    
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))

        self.checkPassword(self.user)
        return self.cleaned_data

    def checkPassword(self, username):
        user2 = User.objects.get(username=username)
        if not user2.check_password(self.cleaned_data.get('userPassword')):
            raise forms.ValidationError(_(u'Password incorrect, try again'))

    def hasNewPassword(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != "" and self.cleaned_data['password2'] != "":
                return True
        return False
    
    def getNewPassword(self):
        return self.cleaned_data['password1']

    def hasNewFirstName(self):
        if 'firstname' in self.cleaned_data and self.cleaned_data['firstname'] != "":
            return True
        return False
 
    def getNewFirstName(self):
        return self.cleaned_data['firstname']

    def hasNewLastName(self):
        if 'lastname' in self.cleaned_data and self.cleaned_data['lastname'] != "":
            return True
        return False
 
    def getNewLastName(self):
        return self.cleaned_data['lastname']

class RegistrationForm(forms.Form):
    
    firstname = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=30)),
                                label=_(u'First Name'))
    lastname = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=30)),
                               label=_(u'Last Name'))

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'Email Address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'Confirm Password'))
 
    def clean_email(self):
        
        try:
            user = User.objects.get(email=self.cleaned_data.get('email'))
        except User.DoesNotExist:
            return self.cleaned_data.get('email')
        raise forms.ValidationError(_(u'This email is already taken. Please choose another.'))

    def clean(self):
        
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data
    
    def save(self, commit=True):
        
        currentBool = False
        size = 30
        chars = string.ascii_letters + string.digits
        while not currentBool:
            username = ''.join(random.choice(chars) for x in range(size))
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:
                currentBool = True
        
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        firstname = self.cleaned_data.get('firstname')
        lastname = self.cleaned_data.get('lastname')
   
        self.new_user = User.objects.create_user(username, email, password)
        self.new_user.first_name = firstname
        self.new_user.last_name = lastname

        self.new_user.save()

	self.user_cache = authenticate(username=username,
                                       password=self.cleaned_data['password1'])
        return self.new_user

    def get_user(self):
        return self.user_cache
