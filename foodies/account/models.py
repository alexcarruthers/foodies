from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission
from foodies.utils import disable_for_loaddata

class UserProfile(models.Model):
   user = models.OneToOneField(User)

   # Other fields here
   def __unicode__(self):
      return self.user.username

@disable_for_loaddata
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile object for each user on creation.
    """
    if created:
        UserProfile.objects.create(user=instance)
        add_recipe_permission = Permission.objects.get(codename="add_recipe")
        delete_recipe_permission = Permission.objects.get(codename="delete_recipe")
        change_recipe_permission = Permission.objects.get(codename="change_recipe")
        view_recipe_permission = Permission.objects.get(codename="view_recipe")

        add_blog_permission = Permission.objects.get(codename="add_blogpost")
        delete_blog_permission = Permission.objects.get(codename="delete_blogpost")
        change_blog_permission = Permission.objects.get(codename="change_blogpost")

        instance.user_permissions.add(
                add_recipe_permission, delete_recipe_permission, change_recipe_permission,
                add_blog_permission, delete_blog_permission, change_blog_permission
                )

post_save.connect(create_user_profile, sender=User)
