# -*- coding: utf-8 -*-
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign
from django.contrib.auth.models import User

from models import BlogPost
from forms import BlogPostForm

@login_required
def create_update_post(request, pk=None):
    post = None
    if pk:
        post = get_object_or_404(BlogPost, pk=pk)
        if not request.user.has_perm("blog.change_blogpost", post):
            return HttpResponseForbidden()
    else:
        if not request.user.has_perm("blog.add_blogpost"):
            return HttpResponseForbidden()

    # Do an update.
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():  # All validation rules pass
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            assign('blog.view_blogpost', request.user, post)
            assign('blog.change_blogpost', request.user, post)
            assign('blog.delete_blogpost', request.user, post)

            return redirect(reverse('view_post', args=[post.id]))
    else:
        form = BlogPostForm(instance=post)  # An unbound form

    # Return the crud page.
    return render_to_response('blog/create_edit_post.xhtml', {
        'post': post, 'form': form
    }, context_instance=RequestContext(request))


def view_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render_to_response('blog/view_post.xhtml', {'post': post},
                              context_instance=RequestContext(request))


def list_user_blogs(request, pk):
    thisuser = get_object_or_404(User, pk=pk)
    blog_list = BlogPost.objects.filter(user=thisuser).order_by('-created')
    return render_to_response('blog/listblogs.html', {'blog_list': blog_list,
                                                      'username': thisuser.get_full_name()},
                              context_instance=RequestContext(request))


def list_blogs(request):
    blog_list = BlogPost.objects.order_by('-created')
    return render_to_response('blog/listblogs.html', {'blog_list': blog_list},
                              context_instance=RequestContext(request))

@login_required
def delete_post(request, pk):
    try:
        post = BlogPost.objects.get(pk=pk)
        if not request.user.has_perm('blog.delete_blogpost', post):
            return HttpResponseForbidden()
        post.delete()
    except BlogPost.DoesNotExist:
        raise Http404
    return redirect(reverse('list_posts'))


@login_required
def list_my_posts(request):
    blog_list = BlogPost.objects.filter(user=request.user).order_by('-created')
    return render_to_response('blog/listblogs.html', {'blog_list': blog_list,
                                                          'username': request.user.get_full_name()},
                              context_instance=RequestContext(request))

def search_blogs(request):
    final_list = []
    search_input = ''
    if 'searchInput' in request.GET:
        search_input = request.GET['searchInput']
        if search_input != None and search_input.strip() != '':
            blog_list = BlogPost.objects.order_by('-created')
            splitInput = search_input.split()
            sorting_list = []
            for blog in blog_list:
                searchedRecipe = searchObject(blog, splitInput)
                if searchedRecipe.is_not_none():
                    sorting_list.append(searchedRecipe)

            sorted_list = sorted(sorting_list, key = lambda x: (x.titleCount, x.userCount, x.bodyCount), reverse=True)

            for item in sorted_list:
                final_list.append(item.blog)
        else:
            search_input = ''
            final_list = []
    else:
        final_list = []
    return render_to_response('blog/search.html', {'blog_list':
        final_list, 'input_value':'+'.join(search_input.split())}, context_instance=RequestContext(request))

class searchObject():
    def __init__(self, blog, splitInput):
        self.titleCount = 0
        self.userCount = 0
        self.bodyCount = 0
        self.blog = blog
        self.calculateCount(splitInput)

    def is_not_none(self):
        total = self.titleCount + self.userCount + self.bodyCount
        if total == 0:
            return False
        else:
            return True

    def calculateCount(self, splitInput):
        for i in splitInput:
            self.titleCount = self.blog.title.lower().split().count(i.lower())
            self.userCount = self.blog.user.get_full_name().lower().split().count(i.lower())
            self.bodyCount = self.blog.body.lower().split().count(i.lower())
