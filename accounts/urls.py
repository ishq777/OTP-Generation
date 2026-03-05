from .import views
from django.urls import path, include

urlpatterns = [

    path('send_otp/', views.send_otp, name='sent_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp')
]
