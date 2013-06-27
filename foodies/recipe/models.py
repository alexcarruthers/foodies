from django.core.urlresolvers import reverse
from django.db import models
from djangoratings.fields import RatingField
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel


class Recipe(TimeStampedModel):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    prep_steps = models.TextField()
    time_to_prepare = models.IntegerField()
    cooking_time = models.IntegerField()
    image = models.ImageField(upload_to='photos/%Y/%m/%d', max_length=100, blank=True)
    rating = RatingField(range=5)

    is_public = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('view_recipe', args=[str(self.id)])

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ("view_recipe", "Can view the recipe"),
        )


class Ingredient(models.Model):
    UNITS_CHOICES = (
        ('tsp', 'teaspoon'),
        ('tbsp', 'tablespoon'),
        ('fl oz', 'fluid ounce'),
        ('c', 'cup'),
        ('pt', 'pint'),
        ('qt', 'quart'),
        ('gal', 'gallon'),
        ('mL', 'milliliter'),
        ('L', 'liter'),
        ('lb', 'pound'),
        ('oz', 'ounce'),
        ('g', 'gram'),
        ('kg', 'kilogram'),
        (' ', 'unit'),
    )
    recipe = models.ForeignKey(Recipe, related_name='ingredients')
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=8, choices=UNITS_CHOICES)

    def __unicode__(self):
        return str(self.quantity) + self.unit + ' ' + self.name
