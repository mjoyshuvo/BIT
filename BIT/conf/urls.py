from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path
from apps.home.views import *
from apps.api import urls as api_urls

urlpatterns = [
    path('', home, name='home'),
    path('git_redirect', git_redirect, name='home'),
    path('webhook', web_hook, name='webhook'),
    url(r'^get_repo/(?P<repo>[\w\d\-]+)/$', get_repo, name='get_repo'),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    url(r'^api/v1/', include(api_urls, 'api_v1'))
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)