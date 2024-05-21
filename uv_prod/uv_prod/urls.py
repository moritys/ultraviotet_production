from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path('', include('homepage.urls')),
    path('catalog/', include('catalog.urls')),
    path('production/', include('production.urls')),
    path('shopping/', include('shopping.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
