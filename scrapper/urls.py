# urls

from django.contrib import admin
from django.urls import path
from . import views

app_name = 'scrapper'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_loopnet/', views.loopnet, name='search_results'),
    path('search_results/download-csv/', views.csv_loopnet, name='download_csv'),
    path('search_Showcase/', views.showcase, name='search_Showcase'),

]