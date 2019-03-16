from django.contrib.sitemaps import Sitemap
from peripteras.kiosks.models import Kiosk


class KioskSitemap(Sitemap):
    changefreq = "never"
    priority = 1

    def items(self):
        return Kiosk.objects.all()

    def location(self, obj):
        return '/kiosk/' + str(obj.id)
