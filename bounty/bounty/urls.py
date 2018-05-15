from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^projects/', include('projects.urls')),
    url(r'^hq/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'', include('projects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# TODO - move this into a more logical file.
admin.site.site_header = 'BOUNTY Headquarters'
admin.site.index_title = 'Dashboard'
admin.site.site_title = 'BOUNTY Headquarters'
