"""peripteras URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import patterns, include, url, handler400, handler403, handler404, handler500

from django.contrib import admin

from peripteras.sitemaps import KioskSitemap

sitemaps = {
    'kiosks': KioskSitemap
}


admin.site.site_header = 'Super root panel'
admin.site.site_title = 'Super root'

urlpatterns = patterns(
    '',
    url(r'', include('peripteras.public.urls', 'public')),

    url(r'', include('peripteras.users.urls', 'users')),

    url(r'', include('peripteras.kiosks.urls', 'managers')),

    # API URL
    url(r'^api/', include('peripteras.public.api.urls')),

    # User API URL
    url(r'^user/api/', include('peripteras.users.api.urls')),

    # Kiosk managers API URL
    url(r'^managers/api/', include('peripteras.kiosks.api.urls')),

    # sitemap and robots
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    # url(r'^robots.txt$', include('robots.urls')),


    # API URL
    # url(r'^api/', include('peripteras.public.api.urls')),

    # Admin URLs
    url(r'^admin/', include(admin.site.urls)),

    # SimpleUsers URLs
    # url(r'^user/', include('peripteras.users.urls', 'user')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})

)
