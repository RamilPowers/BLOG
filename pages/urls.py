from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('contacts/', views.get_contact,  name='contact'),
    path('about/', views.AboutListView.as_view(), name='about'),
    path('fuel-calc', views.get_fuel, name='fuel_calculator'),
    path('kfactor-calc', views.get_kfactor, name='kfactor_calculator'),
    path('<slug:slug>/', views.get_post_detail, name='post_detail'),
    path('', views.PostListView.as_view(), name='post_list'),
]

