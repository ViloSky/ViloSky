from django.urls import path
from django.urls import include
from django.conf import settings
from ViloSkyApp import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.login, name='login'),
    path('register/',views.register, name='register'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('mydetails/',views.mydetails, name='mydetails'),
    path('myactions/',views.myactions, name='myactions'),
    path('report/',views.report, name='report'),
    path('roles/',views.roles, name='roles'),
]