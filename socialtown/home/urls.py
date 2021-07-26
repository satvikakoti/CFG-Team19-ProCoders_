from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('registervol/', views.registervol, name='registervol'),
    path('registerngo/', views.registerngo, name='registerngo'),
    path('home/', views.home, name='home2'),
    path('charts_view/', views.charts_view, name='charts'),
    path('corporate_view/', views.corporate_view, name='corporate'),
    path('ngoAnalysis_view/', views.ngoAnalysis_view, name='ngoAnalysis'),
    path('tables_view/', views.tables_view, name='tables'),
    path('home_user/', views.home_user, name='home_user'),
    path('homengo/', views.homengo, name='homengo'),
]

