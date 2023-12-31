# urls

from django.contrib import admin
from django.urls import path
from . import views

app_name = 'scrapper'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_loopnet/', views.loopnet, name='search_results'),
    path('search_crexi_results/', views.crexi, name='search_results_c'),
    path('search_results/download-csv/', views.Csv, name='download_csv'),
    path('search_Showcase/', views.showcase, name='search_Showcase'),
    path('search_crexi/', views.crexi, name='search_Crexi'),
    path('search_propertysharks/', views.propertysharks, name='search_propertysharks'),
    path('search/', views.search, name='search'),
    path('search_at_once/', views.search_at_once, name='search_at_once'),
]