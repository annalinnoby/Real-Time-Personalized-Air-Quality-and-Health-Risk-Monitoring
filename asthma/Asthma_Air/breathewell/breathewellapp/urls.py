from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('personal/', views.personal, name='personal'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('userhome/', views.userhome, name='userhome'),



    path('realtimedata/', views.realtimedata, name='realtimedata'),
    path('risklevels/', views.risklevels, name='risklevels'),
    path('forecast/', views.forecast, name='forecast'),
    path('historicaldata/', views.historicaldata, name='historicaldata'),
    path('historicaldataapi/<str:timeframe>/', views.historicaldataapi, name='historicaldataapi'),
    path('routeoptimization/', views.routeoptimization, name='routeoptimization'),
    path('about/', views.about, name='about'),

]
