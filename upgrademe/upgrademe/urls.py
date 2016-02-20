"""foober URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from views import *
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', populate_home_page),
    url(r'^browse/$', populate_browse),
    url(r'^browse/([0-9]+)$', populate_long_offer),
    url(r'^confirm/([0-9]+)$', confirm_request),
    url(r'^request/([0-9]+)$', request_food),
    url(r'^accept/([0-9]+)$', accept_request),
    url(r'^register/$', get_new_user),
    url(r'^thanks/$', populate_user_created),
    url(r'^offer/$', get_new_offer),
    url(r'^thanks/offer/([0-9])$', thank_offer),
    url(r'^login/$', login, {'template_name': 'log_in.html'}),
    url(r'^login/?next=(.*)$', login, {'template_name': 'log_in.html'}),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^static/(.*)', return_static_file),
    url(r'^accounts/profile/$', see_profile),
    url(r'^admin/', include(admin.site.urls)),
]
