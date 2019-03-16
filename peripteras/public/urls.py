from django.conf.urls import include, patterns, url


urlpatterns = patterns(
    # URL endpoints for feedback.
    'peripteras.public',

    # Home page
    url('^$', 'views.home', name='home'),

    # Info
    # url('^first-step/$', 'views.first_step', name='first_step'),

    # Address page
    url('^second-step/$', 'views.second_step', name='second_step'),

    # Kiosks page
    # url('^third-step/$', 'views.third_step', name='third_step'),

    # Kiosk main page
    url('^kiosk/(?P<id>[\d]+)/', 'views.kiosk', name='kiosk'),

    # All Kiosks
    url('^kiosks/all/', 'views.all_kiosks', name='all_kiosks'),

    # Areas
    url('^areas/', 'views.areas', name='areas'),

    # Zoho
    url('^zohoverify/verifyforzoho.html', 'views.zoho', name='zoho'),

    # Contact
    url('^contact', 'views.contact', name='contact'),

    # How
    url('^how', 'views.how', name='how'),

    # Terms
    url('^terms', 'views.terms', name='terms'),

    # faq
    url('^faq', 'views.faq', name='faq'),

    
    # 404 page
    # url('sorry/', 'views.sorry404', name='sorry404'),

    # 500 page
    # url('error/', 'views.sorry500', name='sorry500'),
    
   

)