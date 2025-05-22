from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from blog.views import CustomLogoutView

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/logout/', CustomLogoutView.as_view(), name="logout"),
    path('auth/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
