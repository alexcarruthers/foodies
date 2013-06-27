from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class MainPageTests(TestCase):
    def test_main_page_anonymous(self):
        c = Client()
        response = c.get(reverse('mainpage'))

        self.failUnlessEqual(response.status_code, 200)

        # There is no view function but there is the default Request Context that is past to the template.
        assert "Sign In" in response.content
        assert "Recipes" in response.content
        assert "Search Recipes" in response.content
        assert "Blog Posts" in response.content


    def test_main_page_loggedin(self):
        user = User.objects.create_superuser("test", "test@test.com", "test")

        c = Client()
        c.login(username='test', password='test')
        response = c.get(reverse('mainpage'))

        self.failUnlessEqual(response.status_code, 200)

        # There is no view function but there is the default Request Context that is past to the template.
        assert "Sign In" not in response.content
        assert "Recipes" in response.content
        assert "Search Recipes" in response.content
        assert "Blog Posts" in response.content
        assert "New Recipe" in response.content
        assert "My Blog Posts" in response.content
        assert "New Blog Post" in response.content
