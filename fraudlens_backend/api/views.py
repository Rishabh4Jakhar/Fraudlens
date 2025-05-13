from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ai_models import trust, smsScam
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AppUser
"""
# Hash password
hashed_pwd = make_password(password)

# Check password
if check_password(plain_password, hashed_pwd):
    # Password matches

# Signup
hashed_pwd = make_password(password)
AppUser.objects.create(username=username, email=email, password=hashed_pwd)

# Login
user = AppUser.objects.get(username=username)
if check_password(password, user.password):
    # Login success
else:
    # Invalid credentials

        
"""

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not (username and email and password):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        if AppUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=409)

        hashed_pwd = make_password(password)
        AppUser.objects.create(username=username, email=email, password=hashed_pwd)

        return JsonResponse({'message': 'User registered successfully'})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not (username and password):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        try:
            user = AppUser.objects.get(username=username)
            if check_password(password, user.password):
                # Login success
                return JsonResponse({'message': 'Login successful', 'username': user.username})            
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except AppUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)



@api_view(['POST'])
def check_website_trust(request):
    url = request.data.get('url', '')
    # Here, you'll later call the AI function
    response = trust.run_trust(url)
    #print(response, "In api call", url)
    #response = {"trust_score": 78, "message": f"Website seems safe {url}"}  
    return JsonResponse(response)

@api_view(['POST'])
def detect_scam_email(request):
    email_text = request.data.get('email_text', '')
    # Call AI function here later
    response = {"scam_probability": 92, "message": "Likely a phishing attempt"}
    return JsonResponse(response)

@api_view(['POST'])
def check_sms_scam(request):
    sms_text = request.data.get('sms_text', '')
    # Call AI function here later
    response = {"scam_probability": 90, "message": "Likely a scam"}
    return JsonResponse(response)