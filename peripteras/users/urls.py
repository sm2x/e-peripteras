from django.conf.urls import include, patterns, url
from django.contrib.auth import views as auth_views

from peripteras.users.forms import LoginAuthenticationForm


urlpatterns = patterns(
    'peripteras.users',

    # Private area "/user" is difined at main urls.py
    # url(r'^login/$',
    #     auth_views.login,
    #     {'template_name': 'users/login.html',
    #      'authentication_form': LoginAuthenticationForm},
    #     name='auth_login'),
    # url(r'^password/change/$',
    #     'views.password_change',
    #     name='password_change'),
    
    # Register new user
    # url('^register/$', 'views.register', name='register'),

    # Non django style for user login
    # url('^login/$', 'views.custom_login', name='custom_login'),

    url(r'^login/$',
        auth_views.login,
        {'template_name': 'users/login.html',
         'authentication_form': LoginAuthenticationForm},
        name='auth_login'),

    # Register users
    url('^register/$', 'views.register', name='register'),

    # Register manager
    url('^manager/register$', 'views.register_manager', name='register_manager'),

    # Logout user
    url(r'^logout/$',
        auth_views.logout,  {'next_page': '/'}, name='logout'),

    #View Basket
    url('^basket/(?P<kiosk_id>[\d]+)/', 'views.basket', name='basket'),

    #View complete info
    url('^order/(?P<kiosk_id>[\d]+)/completed/', 'views.completed', name='order_completed'),

    #View Basket
    url('^feedback/(?P<order_id>[\d]+)/add', 'views.add_feedback', name='add_feedback'),



)

