from django.urls import path

from . import views

urlpatterns = [
   path('',views.index,name='index'),
   path('parkatdcu/carparks/',views.carparks,name='carparks'),
   path('bus/campus/',views.campus,name='campus'),
   path('bus/bus/',views.bus,name='bus'),
]
