from django.urls import path
from .views import *
urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    path('',dashboard,name='dashboard'),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('forgotPassword/',forgotPassword ,name='forgotPassword'),
    path('restpassword_validate/<uidb64>/<token>/',restpassword_validate, name='restpassword_validate'),
    path('resetPassword/',resetPassword ,name='resetPassword'),

]
