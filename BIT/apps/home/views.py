from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from conf.settings import CLIENT_ID
from apps.user.models import UserProfile, OauthCode


@login_required(login_url='/login/')
def home(request):
    title = 'DjangoProject'
    client_id = CLIENT_ID
    return render(request, 'home.html', {'title': title, 'client_id': client_id})


def git_redirect(request):
    title = 'redirect page'
    user = request.user
    code = request.GET['code']
    if user:
        try:
            oauth_data = OauthCode.objects.get(user=user)
            oauth_data.code = code
            oauth_data.save()
        except OauthCode.DoesNotExist:
            oauth_data = OauthCode.objects.create(user=user, code=code)
        print(oauth_data)
    return render(request, 'redirect.html', {'title': title})


def git_oauth(request):
    params = {'client_id': '23f083fd33cdcbc76754', 'redirect_uri': 'http://0.0.0.0:8000/git_redirect', 'scope': 'repo',
              'state': 'state',
              'login': 'mjoyshuvo', 'allow_signup': True}
    oauth_url = 'https://github.com/login/oauth/authorize'
    r = requests.get(url=oauth_url, params=params)
    print(r)
    return HttpResponse("OK")
