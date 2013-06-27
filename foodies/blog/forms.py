from django.forms import ModelForm, Textarea, TextInput, ModelChoiceField

from foodies.recipe.models import Recipe

from models import BlogPost

class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('user',)
        widgets = {
            'title': TextInput(attrs={'id': 'inputTitle', 'placeholder': 'Title', 'class': 'input-xxlarge'}),
            'body': Textarea(attrs={'id': 'inputBody', 'placeholder': 'Blog', 'class': 'input-xxlarge'})
        }
        recipe_link = ModelChoiceField(queryset=Recipe.objects.filter(is_public=True).order_by('-created'), required=False)
