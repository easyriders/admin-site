from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import Context

from account.models import UserProfile

from models import Site, PC, PCGroup


@login_required
def index(request):
    user = request.user
    profile = user.get_profile()

    if profile.type == UserProfile.SUPER_ADMIN:
        # Redirect to list of sites
        return redirect('/sites/')
    else:
        # User belongs to one site only; redirect to that site
        site_url = profile.site.url
        return redirect('site/{0}/'.format(site_url))


@login_required
def sites_overview(request):
    site_list = Site.objects.all()
    context = Context({'site_list': site_list})
    return render(request, 'system/sites.html', context)


simple_context = lambda s: {'site': s}


def site_view(template, get_context=simple_context):
    """Return a function which will generate a site view and render it with
    "template" and use "processor" to add context as necessary."""
    @login_required
    def _site_view(request, site_uid):
        uid = site_uid.upper()
        site = get_object_or_404(Site, uid=uid)
        context = get_context(site)
        return render(request, template, context)

    return _site_view


# Now follows all site-based views as generated by the _site_view_ function.
# TODO: Define get_context functions as needed.

site = site_view('system/site_overview.html')
configuration = site_view('system/site_configuration.html')
jobs = site_view('system/site_jobs.html')
scripts = site_view('system/site_scripts.html')


def computers(request, site_uid, uid=None):
    """Special handling of computers view."""
    def get_computers_context(site):
        if not uid and site.pcs.count() >= 1:
            selected = site.pcs.all()[0]
        elif not uid:
            selected = None
        else: 
            selected = get_object_or_404(PC, uid=uid)
        
        context = simple_context(site)
        context['selected_pc'] = selected
        return context

    view =  site_view('system/site_computers.html', get_computers_context)

    return view(request, site_uid)


def groups(request, site_uid, uid=None):
    """Special handling of groups view."""
    def get_groups_context(site):
        if not uid and site.groups.count() >= 1:
            selected = site.groups.all()[0]
        elif not uid:
            selected = None
        else:
            uid = uid.upper()
            selected = get_object_or_404(PCGroup, uid=uid)
        
        context = simple_context(site)
        context['selected_group'] = selected
        return context

    view =  site_view('system/site_groups.html', get_groups_context)

    return view(request, site_uid)


def users(request, site_uid, uid=None):
    """Special handling of users view."""
    def get_users_context(site):
        if not uid and len(site.users) >= 1:
            selected = site.users[0]
        elif not uid:
            selected = None
        else:
            selected = get_object_or_404(User, username=uid)
        
        context = simple_context(site)
        context['selected_user'] = selected

        choices = selected.get_profile().type_choices
        choices_dict =[{'id': k, 'val': v} for (k, v) in choices] 

        context['choices'] = choices_dict

        return context

    view = site_view('system/site_users.html', get_users_context)

    return view(request, site_uid)
