from apps.userprofile.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from actstream.models import actor_stream


@login_required
def list_userprofiles(request):
    profile_list = UserProfile.objects.all()
    return render(request, 'userprofile/list_userprofiles.html',
                  {'profile_list': profile_list})


@login_required
def userprofile_detail(request, userprofile_id):
    profile = get_object_or_404(UserProfile, pk=userprofile_id)
    activities = actor_stream(profile.user)
    paginator = Paginator(activities, 50, allow_empty_first_page=True)  # Show 50 activities per page
    page = request.GET.get('page')
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        activities = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        activities = paginator.page(paginator.num_pages)
    total_activities = '{:,}'.format(activities.paginator.count)
    return render(request, 'userprofile/userprofile_detail.html',
            {'profile': profile, 'activities': activities, 'total_activities': total_activities})
