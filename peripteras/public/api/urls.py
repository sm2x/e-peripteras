from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from peripteras.public.api.views import ReadOnlyKiosksAPIView, ReadOnlyKioskItemsAPIView

router = DefaultRouter()

urlpatterns = patterns(
    '',
    url(r'^kiosks/$', ReadOnlyKiosksAPIView.as_view({'get': 'list'}), name='kiosks'),
    url(r'^kiosk/items/$', ReadOnlyKioskItemsAPIView.as_view({'get': 'list'}), name='kiosk_items'),

)
