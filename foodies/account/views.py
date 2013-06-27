from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site

# Monkey Patch Django Login View
from forms import EmailAuthenticationForm as AuthenticationForm
from forms import RegistrationForm, updateUserForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def updateUser(request, success_url=None, 
               form_class=updateUserForm, profile_callback=None,
               template_name='registration/updateUser.html',
               extra_context=None):
    success_url = '/'
    if not request.user.is_authenticated():
        raise Http404
    
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        form.user = request.user
        if form.is_valid():
            if form.hasNewPassword():
                request.user.set_password(form.getNewPassword())
            if form.hasNewFirstName():
                request.user.first_name = form.getNewFirstName()
            if form.hasNewLastName():
                request.user.last_name = form.getNewLastName()
            request.user.save()
           
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
        form.user = request.user

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)


@login_required
def delete_user(request):
    try:
        request.user.delete()
    except:
        raise Http404
    return HttpResponseRedirect('/')
    
def register(request, success_url=None,
             form_class=RegistrationForm, profile_callback=None,
             template_name='registration/register.html',
             extra_context=None):

    success_url = '/'
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save()
	    auth_login(request, form.get_user())
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)
