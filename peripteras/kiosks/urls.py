from django.conf.urls import include, patterns, url


urlpatterns = patterns(
    'peripteras.kiosks',


    # View kiosk dashboard
    url('^kiosk/dashboard/', 'views.kiosk', name='kiosk_dashboard'),

    # Kiosk info page
    url('^kiosk/info', 'views.kiosk_info', name='kiosk_info'),

    # View kiosk help
    url('^kiosk/help/', 'views.help', name='help'),

    # View order
    url('^kiosk/view/order/(?P<order_id>[\d]+)',
        'views.order', name='view_order'),

    # Ficnish order
    url('^kiosk/order/(?P<order_id>[\d]+)/complete',
        'views.complete_order', name='complete_order'),

    # Ficnish order
    url('^kiosk/items/all', 'views.all_items', name='all_items'),

    # Edit an item
    url('^kiosk/item/(?P<item_id>[\d]+)/edit',
        'views.item_edit', name='item_edit'),

    # Add an item
    url('^kiosk/item/add', 'views.item_add', name='item_add'),

    # Delete an item
    url('^kiosk/item/(?P<item_id>[\d]+)/delete',
        'views.item_delete', name='item_delete'),

    # upload_list
    url('^kiosk/item/upload', 'views.upload_list', name='upload_list'),


)
