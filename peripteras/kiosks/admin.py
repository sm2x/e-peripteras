from django.contrib import admin

from peripteras.kiosks.models import KioskManager, Kiosk, Item, Category, Brand, Support

from import_export.admin import ImportExportModelAdmin


@admin.register(KioskManager)
class KioskManagerAdmin(admin.ModelAdmin):
    model = KioskManager
    list_display = ('user', 'kiosk')


@admin.register(Kiosk)
class KioskAdmin(admin.ModelAdmin):
    model = Kiosk


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    model = Item
    list_display = ('title', 'price', 'id', 'kiosk', 'ksk_id', )

    def ksk_id(self, obj):
        return obj.kiosk.id
    ksk_id.short_description = 'Kiosk ID'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ('title', 'id', )


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    model = Support
    list_display = ('subject', 'kiosk')
