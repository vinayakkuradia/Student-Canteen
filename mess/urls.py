from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('order/', views.process_order, name='order'),
    path('myorders/', views.myorders, name='myorders'),
    path('logout/', views.logout, name='logout'),
]
