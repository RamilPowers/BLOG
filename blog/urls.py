from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.login, name='login'),
    path('accounts/password_reset/', views.password_reset, name='password_reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('account.urls')),
    path('', include('social_django.urls')),
    path('', include('pages.urls', namespace='pages')),
    path('ckeditor/', include('ckeditor_uploader.urls')),      
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
