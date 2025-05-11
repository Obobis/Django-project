from lib2to3.fixes.fix_dict import iter_exempt

from django.contrib import admin
from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^posts/', include(('pages1.urls', 'posts'),
                       namespace='posts')),
    re_path(r'^account/', include(('account.urls', 'account'), namespace='account')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
