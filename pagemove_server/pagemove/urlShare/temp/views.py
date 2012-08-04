from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction

from .forms import URLForm
from urlShare.models import User, URL, Device
from twython import Twython
import settings

from urlShare.http_json_response import HttpJSONResponse

mobile_ua_hints = [ 'ipad', 'ipod', 'iphone' ]

def index(request):
    return render(request, 'appUrlLoader.html',)


def twitter_user_required(view_fn):
    def view_wrapper(request):
        if not request.twitter_user:
            request.session['is_ipad'] = request.GET.get('is_ipad')
            return redirect('twitter_login')

        return view_fn(request)

    return view_wrapper


@twitter_user_required
@transaction.commit_on_success
def saveUrl(request):

    url = request.GET.get("url", None)
    form = URLForm(request.POST or None, initial={
        'url': url
    })

    is_ipad = request.session.get('is_ipad')
    twitter_id = request.twitter_user

    if form.is_valid():
        url = form.save(commit=False)
        url.user = twitter_id
        url.save()

        if not is_ipad:
            url.broad_cast()

        return redirect('saveUrl')

    try:
        last_url = request.twitter_user.url_set.order_by('-date_created')[:1].get().url
    except URL.DoesNotExist:
        last_url = None

    

    if is_ipad:
        is_ipad_login = 'true'
    else:
        is_ipad_login = 'false'

    return render(request, 'urlPostForm.html', {
        'form': form,
        'last_url': last_url,
        'is_ipad_login': is_ipad_login,
        'twitter_id': request.twitter_user,
    })


def validToken(request):
    return HttpResponse("true" if request.twitter_user else "false")


def getLastPage(request):
    twitter_id = request.GET.get("twitter_id")
    last = get_object_or_404(URL.objects
                             .filter(user__twitter_id=twitter_id)
                             .order_by('-date_created')[:1])

    return HttpJSONResponse({'url': last.url})


def getHistory(request):
    twitter_id = request.GET.get("twitter_id")
    userUrlCheak = (URL.objects
                    .filter(user__twitter_id=twitter_id)
                    .order_by('-date_created'))

    return HttpJSONResponse({'url': [o.url for o in userUrlCheak]})


def ios(request):
    return render(request, 'ios.html',)


def googleVerify(request):
    return render(request, 'google9bb880dc94f5c6e5.html',)


def normalize_device_id(raw_device_id):
    return raw_device_id.replace("<", "").replace(">", "").replace(" ", "")


def begin_auth(request):
    """
        The view function that initiates the entire handshake.
        For the most part, this is 100% drag and drop.
    """

    # Instantiate Twython with the first leg of our trip.
    twitter = Twython(
        twitter_token=settings.TWITTER_KEY,
        twitter_secret=settings.TWITTER_SECRET,
        callback_url=request.build_absolute_uri(reverse('urlShare.views.thanks'))
    )

    # Request an authorization url to send the user to...
    auth_props = twitter.get_authentication_tokens()

    # Then send them over there, durh.
    request.session['request_token'] = auth_props
    return HttpResponseRedirect(auth_props['auth_url'])


def thanks(request):
    """A user gets redirected here after hitting Twitter and authorizing your app to use their data.
        ***
            This is the view that stores the tokens you want
            for querying data. Pay attention to this.
        ***
    """

    # Now that we've got the magic tokens back from Twitter, we need to exchange
    # for permanent ones and store them...
    twitter = Twython(
        twitter_token=settings.TWITTER_KEY,
        twitter_secret=settings.TWITTER_SECRET,
        oauth_token=request.session['request_token']['oauth_token'],
        oauth_token_secret=request.session['request_token']['oauth_token_secret'],
    )

    # Retrieve the tokens we want...
    authorized_tokens = twitter.get_authorized_tokens()
    twitter_id = authorized_tokens['user_id']
    request.session['twitter_id'] = twitter_id

    if not User.objects.filter(twitter_id=twitter_id).exists():
        user = User.objects.create(twitter_id=twitter_id)

    return redirect('index')


def regisert_device(request):
    twitter_id = request.GET.get('twitter_id')
    device_id = request.GET.get('device_id')
    user = User.objects.get(twitter_id=twitter_id)
    user.device_set.create(device_id=device_id)
    """if not User.objects.filter(twitter_id=twitter_id).exists():
        user = User.objects.create(twitter_id=twitter_id)

    if not Device.objects.filter(device_id=device_id).exists():
        user.device_set.create(device_id=device_id)
    """

    return HttpResponse("success")


def bilitz(request):
    return HttpResponse("42")
