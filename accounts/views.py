from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .helpers import generate_otp


@api_view(['POST'])
def send_otp(request):

    phone = request.data.get('phone_number')
    password = request.data.get('password')

    if not (phone and password):
        return Response({"error"})
    

    user, created = User.objects.get_or_create(phone_number=phone)

    otp = generate_otp()

    user.otp = otp
    print("otp", otp)
    user.set_password(password)
    user.save()

    return Response({"message":"OTP sent"})


@api_view(['POST'])
def verify_otp(request):

    phone = request.data.get('phone_number')
    otp = request.data.get('otp')

    try:
        user = User.objects.get(phone_number=phone)
    except User.DoesNotExist:
        return Response({"error": "user not found"}, status=404)

    if user.otp == otp:
        user.is_number_verified = True
        user.otp = None
        user.save()

        return Response({"message": "OTP verified"})

    return Response({"error": "Invalid OTP"})