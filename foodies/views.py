from django.shortcuts import get_list_or_404, render_to_response
from django.template.context import RequestContext

from foodies.blog.models import BlogPost
from foodies.recipe.models import Recipe


def mainpage(request):
    if request.user.is_authenticated():
        blogs = BlogPost.objects.order_by('-created')[:5]
        recipes = Recipe.objects.order_by('-created')[:5]
        userblogs = BlogPost.objects.filter(user=request.user).order_by('-created')[:5]
        userrecipes = Recipe.objects.filter(user=request.user).order_by('-created')[:5]
        return render_to_response('main.html', {'blogs': blogs, 'recipes': recipes,
                                  'userblogs': userblogs, 'userrecipes': userrecipes},
                                  context_instance=RequestContext(request))
    else:
        blogs = BlogPost.objects.order_by('-created')[:5]
        recipes = Recipe.objects.filter(is_public=True).order_by('-created')[:5]
        return render_to_response('main.html', {'blogs': blogs, 'recipes': recipes},
                           context_instance=RequestContext(request))