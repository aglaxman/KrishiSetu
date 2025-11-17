from django.urls import path
from .views import *
urlpatterns = [
    path('farmer_register/',farmer_register,name='farmer_register'),
    path('farmer_login/',farmer_login,name='farmer_login'),
    path('farmer_logout/',farmer_logout,name='farmer_logout'),
    path('farmer_dashboard/',farmer_dashboard,name='farmer_dashboard'),
    path('farmer_activate/<uidb64>/<token>/',farmer_activate, name='farmer_activate'),
    path('farmer_forgotPassword/',farmer_forgotPassword ,name='farmer_forgotPassword'),
    path('farmer_restpassword_validate/<uidb64>/<token>/',farmer_restpassword_validate, name='farmer_restpassword_validate'),
    path('farmer_resetPassword/',farmer_resetPassword ,name='farmer_resetPassword'),

]
