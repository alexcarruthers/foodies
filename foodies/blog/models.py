from django.db import models
from djangoratings.fields import RatingField
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from foodies.recipe.models import Recipe


class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=200)
    body = models.TextField()
    rating = RatingField(range=5)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', height_field=300, width_field=300, max_length=100, blank=True)

    user = models.ForeignKey(User)
    recipe_link = models.ForeignKey(Recipe, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ("view_blogpost", "Can view the blog post"),
        )

    def __unicode__(self):
        return self.title

