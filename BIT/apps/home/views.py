from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from apps.user.models import UserProfile, OauthCode, SelectedRepos
from conf.settings import CLIENT_ID, CLIENT_SECRET, GIT_USERNAME
from github import Github


@login_required(login_url='/login/')
def home(request):
    title = 'BITS Project'
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
        oauth_data.access_token = access_token
        oauth_data.save()
        git = Github(access_token)
        public_repos = git.get_user().get_repos(type='public')

    return render(request, 'redirect.html', {'title': title, 'public_repos': public_repos})


def get_repo(request, repo):
    client_id = CLIENT_ID
    try:
        oauth_data = OauthCode.objects.get(user=request.user)
        access_token = oauth_data.access_token
        if access_token:
            git = Github(access_token)
            print(repo)
            repo_obj = git.get_repo(GIT_USERNAME+"/"+repo)
            print(repo_obj)
            name = repo_obj.name
            stars = repo_obj.stargazers_count
            SelectedRepos.objects.create(user=request.user, repo_name=name, stars=stars)
            """Creating Webhook"""
            repo_obj = git.get_repo("{owner}/{repo_name}".format(owner=GIT_USERNAME, repo_name=repo))
            events = ["push", "pull_request"]
            config = {
                "url": "http://{host}/{endpoint}".format(host='http://0.0.0.0:8000', endpoint='webhook'),
                "content_type": "json"
            }
            web_hook = repo_obj.create_hook("web", config, events, active=True)
            print(web_hook)
            return HttpResponse("ok")
        else:
            return render(request, 'home.html', {'title': 'BITS Project', 'client_id': client_id})
    except OauthCode.DoesNotExist:
        return render(request, 'home.html', {'title': 'BITS Project', 'client_id': client_id})
