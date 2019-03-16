from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from peripteras.kiosks.api.views import GetAllOrders 

router = DefaultRouter()

urlpatterns = patterns(
    '',
    url(r'^orders/all/$', GetAllOrders.as_view(), name='get_all_orders'),
    # url(r'^basket/add/$', AddToBasket.as_view(), name='basket_add'),
    # url(r'^basket/remove/$', RemoveFromBasket.as_view(), name='basket_get'),

)
