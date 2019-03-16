from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from peripteras.users.api.views import AddToBasket, GetFromBasket, RemoveFromBasket

router = DefaultRouter()

urlpatterns = patterns(
    '',
    url(r'^basket/get/$', GetFromBasket.as_view(), name='basket_get'),
    url(r'^basket/add/$', AddToBasket.as_view(), name='basket_add'),
    url(r'^basket/remove/$', RemoveFromBasket.as_view(), name='basket_get'),

)
