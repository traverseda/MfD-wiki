"""Settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from core.views import signup, login, WikiPage, newWikiPage
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^wiki/(.*)/edit/$', WikiPage.as_view(template_name='wiki/edit.html'), name='wikiEdit'),
    url(r'^wiki/(.*)/revisions/$', WikiPage.as_view(template_name='wiki/revisions.html'), name='wikiRevisions'),
    url(r'^wiki/(.*)/$', WikiPage.as_view(), name='wiki'),
    url(r'^wikiNew/$', newWikiPage, name='wikiNew'),

#    url(r'^comments/', include('django_comments.urls')),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/', signup),
    url(r'^wiki/$', RedirectView.as_view(url='/wiki/home', permanent=False)),
    url(r'^$', RedirectView.as_view(url='/wiki/home', permanent=False),name='home'),
]
