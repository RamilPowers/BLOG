from django.urls import path
from account import views


urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('activate/<uidb64>/<token>', views.account_activate, name='account_activate'),
]