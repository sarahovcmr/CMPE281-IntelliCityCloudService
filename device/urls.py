from django.urls import path, include
from . import views

urlpatterns = [
    path('AddDevice/', views.addDevice),
    path('UpdateDevice/', views.UpdateDeviceInfo),
    path('GetDevice/', views.getDeviceInfo),
    path('GetAllDevices/', views.GetALLDevices),
    path('DeleteDevice/', views.deleteDevice),
    path('UpdateImage/', views.updateImage),
    path('DisableDevice/', views.disableDevice),
    path('GetDeviceOfDistrict/', views.get_device_of_district),
    path('SearchedDevice/', views.GetSearchedDevices),
]

