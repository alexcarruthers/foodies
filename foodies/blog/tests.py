from django.test import TestCase, Client
from foodies.blog.models import BlogPost
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from foodies.recipe.models import Recipe


class ListAllPostsViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        test_user = User.objects.create(username = 'test1')
        test_user2 = User.objects.create(username = 'test2')
        test_user3 = User.objects.create(username = 'test3')

        self.posts = []
        self.posts.append(BlogPost.objects.create(
            title = "Blog post!",
            body = "This is a test blog post",
            user = test_user
        ))
        self.posts.append(BlogPost.objects.create(
            title = "Blog post 2!",
            body = "This is another test blog post",
            user = test_user2
        ))
        self.posts.append(BlogPost.objects.create(
            title = "Blog post 3!",
            body = "This is yet another test blog post",
            user = test_user3
        ))

    def test_views(self):
        response = self.c.get(reverse('list_posts'))
        context_response = response.context['blog_list']

        i = 0
        for test_post in reversed(self.posts):
            test_post_pk = test_post.pk
            resp_post_pk = context_response[i].pk

            self.assertEqual(resp_post_pk, test_post_pk)

            i += 1

class ListUserBlogsViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        test_user = User.objects.create(username = 'test1')
         
        self.posts = []
        self.posts.append(BlogPost.objects.create(
            title = "Blog post!",
            body = "This is a test blog post",
            user = test_user
        ))
        self.posts.append(BlogPost.objects.create(
            title = "Blog post 2!",
            body = "This is another test blog post",
            user = test_user
        ))
        self.posts.append(BlogPost.objects.create(
            title = "Blog post 3!",
            body = "This is yet another test blog post",
            user = test_user
        ))
        self.posts.append(BlogPost.objects.create(
            title = "Blog post 4!",
            body = "This is yet another test blog post",
            user = test_user
        ))
        
        
    def test_views(self):
        response = self.c.get(reverse('list_posts'))
        context_response = response.context['blog_list']

        i = 0
        for test_post in reversed(self.posts):
            test_post_pk = test_post.pk
            resp_post_pk = context_response[i].pk

            self.assertEqual(resp_post_pk, test_post_pk)

            i += 1

class CRUDPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("test", "test@test.com", "test")
        #self.user.user_permissions.add(Permission.objects.get(codename="add_blogpost"))
        self.user.save()

        self.post = BlogPost.objects.create(
            title="MY FIRST POST YAY!",
            body="HELLO WORLD",
            user=self.user
        )
        self.post.save()

    def test_read_post(self):
        c = Client()
        response = c.get(reverse('view_post', args=[self.post.id]))

        self.failUnlessEqual(response.status_code, 200)

        returned_post = response.context['post']
        self.assertEqual(returned_post.title, self.post.title)
        self.assertEqual(returned_post.body, self.post.body)
        self.assertEqual(returned_post.user, self.post.user)

    def test_create_post(self):
        #  NOTE: Validation of user input is tested through django's unit-tests.
        #  The view does not do any special user input validation beyond django's,
        #  so there's no validation tests required.

        c = Client()
        c.login(username='test', password='test')

        response = c.post(reverse('create_post'), {
            "title": "NEW POST",
            "body": "HELLO WORLD",
            "user": self.user.pk
        }, follow=True)

        self.failUnlessEqual(response.status_code, 200)

        post = BlogPost.objects.get(title="NEW POST")

        self.assertEqual(post.user, self.user)
        self.assertEqual(post.title, "NEW POST")
        self.assertEqual(post.body, "HELLO WORLD")
        self.assertTrue(self.user.has_perms('blog.view_blogpost', post))
        self.assertTrue(self.user.has_perms('blog.change_blogpost', post))
        self.assertTrue(self.user.has_perms('blog.delete_blogpost', post))


    def test_update_post(self):
        #  NOTE: Validation of user input is tested through django's unit-tests.
        #  The view does not do any special user input validation beyond django's,
        #  so there's no validation tests required.

        c = Client()
        c.login(username='test', password='test')

        response = c.post(reverse('update_post', args=[self.post.pk]), {
            "title": "POST",
            "body": self.post.body
        }, follow=True)

        self.failUnlessEqual(response.status_code, 200)

        updated_post = BlogPost.objects.get(pk=self.post.pk)
        self.assertEqual(updated_post.title, "POST")

    def test_delete_post(self):
        delete_object = self.post.id
        c = Client()
        c.login(username='test', password='test')
        response = c.get(reverse('delete_post', args=[delete_object]))

        self.failUnlessEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            BlogPost.objects.get(pk=delete_object)

class BlogSearchViewTest(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(
            username='test_username',
            email='test@test.com',
            password='test'
        )
        self.testUser.first_name = 'testFirst'
        self.testUser.last_name = 'testSecond'

        self.testFailureUser = User.objects.create_user(
            username='test_failure_name',
            email='test2@test.com',
            password='test2'
        )
        self.testFailureUser.first_name = 'testThird'
        self.testFailureUser.last_name = 'testFourth'

        self.testUser.save()
        self.testFailureUser.save()

        self.testBlog = BlogPost.objects.create(
            title='test_blog',
            user=self.testUser,
            body='This is a test blog'
        )

        self.testFailureBlog = BlogPost.objects.create(
            title='test_failure_recipe',
            user=self.testFailureUser,
            body='blah'
        )

        self.testBlog.save()
        self.testFailureBlog.save()

        self.url = reverse('search_blogs')

    def test_search_blog_view_renders(self):
        c = Client()
        response = c.get(self.url, data={'searchQuery': ''})

        # Test http response status, url, and html template
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/search.html')
        self.assertTemplateUsed(response, 'blog/listblogs.html')

    def test_search_blog_view_by_title_success(self):
        c = Client()

        response = c.get(self.url, data={'searchInput': self.testBlog.title})
        results = response.context['blog_list']

        self.assertEquals(len(results), 1)
        for res in results:
            self.assertEquals(res.pk, self.testBlog.pk)

    def test_search_blog_view_by_user_success(self):
        c = Client()

        response = c.get(self.url, data={'searchInput': self.testBlog.user.first_name})
        results = response.context['blog_list']

        self.assertEquals(len(results), 1)
        for res in results:
            self.assertEquals(res.user.pk, self.testUser.pk)

        response = c.get(self.url, data={'searchInput': self.testBlog.user.last_name})
        results = response.context['blog_list']

        self.assertEquals(len(results), 1)
        for res in results:
            self.assertEquals(res.user.pk, self.testUser.pk)

    def test_search_blog_view_by_title_failure(self):
        c = Client()

        response = c.get(self.url, data={'searchInput': self.testBlog.title})
        results = response.context['blog_list']

        for res in results:
            self.assertNotEquals(res.pk, self.testFailureBlog.pk)

    def test_search_recipe_view_by_user_failure(self):
        c = Client()

        response = c.get(self.url, data={'searchInput': self.testBlog.user.first_name})
        results = response.context['blog_list']

        for res in results:
            self.assertNotEquals(res.user.pk, self.testFailureUser.pk)

        response = c.get(self.url, data={'searchBlog': self.testBlog.user.last_name})
        results = response.context['blog_list']

        for res in results:
            self.assertNotEquals(res.user.pk, self.testFailureBlog.pk)


class BlogRecipeLinkTest(TestCase):
    def setUp(self):
        self.c = Client();
        self.user = User.objects.create(
        		username = 'test_user_1',
        		password='!',
						first_name='test',
						last_name='user'
        		)
        self.user.set_password('1234')
        self.user.save()
        self.c.login(username='test_user_1', password='1234')
        self.recipe = Recipe.objects.create(
            name="Recipe!",
            user= self.user,
            prep_steps="A B D \n C E F",
            time_to_prepare=5,
            cooking_time=5
        )
        self.recipe2 = Recipe.objects.create(
            name="Recipe2",
            user= self.user,
            prep_steps="A B D \n C E F",
            time_to_prepare=5,
            cooking_time=5
        )
        self.recipe2.save()

        self.post = BlogPost.objects.create(
            title = "Blog post!",
            body = "This is a test blog post",
            user = self.user,
            recipe_link = self.recipe 
        )

    def test_add_link(self):
        response = self.c.post(reverse('create_post'), {
            "title": "NEW POST",
            "body": "HELLO WORLD",
            "user": self.user.pk,
            "recipe_link": self.recipe2.pk
            }, follow=True)
        self.failUnlessEqual(response.status_code, 200)

        context_response = response.context['post']
        self.failUnlessEqual(context_response.recipe_link.name, self.recipe2.name)

        
    def test_view_link(self):
       response = self.c.get(reverse('view_post', args=[self.post.id]))
       self.failUnlessEqual(response.status_code, 200)
       context_response = response.context['post']
       self.assertEqual(context_response.recipe_link.name, self.recipe.name)

