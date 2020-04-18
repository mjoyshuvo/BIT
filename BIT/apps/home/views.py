from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from apps.user.models import UserProfile, OauthCode
from conf.settings import CLIENT_ID, CLIENT_SECRET, GIT_USERNAME
from github import Github


@login_required(login_url='/login/')
def home(request):
    title = 'DjangoProject'
    client_id = CLIENT_ID
    return render(request, 'home.html', {'title': title, 'client_id': client_id})


def git_redirect(request):
    title = 'Redirect page'
    user = request.user
    code = request.GET['code']
    if user:
        try:
            oauth_data = OauthCode.objects.get(user=user)
            oauth_data.code = code
            oauth_data.save()
        except OauthCode.DoesNotExist:
            oauth_data = OauthCode.objects.create(user=user, code=code)
    access_token_url = 'https://github.com/login/oauth/access_token'
    params = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'code': code,
              'redirect_uri': 'http://0.0.0.0:8000/git_redirect'}
    headers = {'Accept': 'application/json'}
    response = requests.post(url=access_token_url, data=params, headers=headers)
    access_token = response.json()['access_token']
    git = Github(access_token)
    public_repos = git.get_user().get_repos(type='public')
    # for repo in git.get_user().get_repos(type='public'):
    #     print(repo.name)

    return render(request, 'redirect.html', {'title': title, 'public_repos': public_repos})

