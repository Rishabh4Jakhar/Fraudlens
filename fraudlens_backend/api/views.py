from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_website_trust(request):
    url = request.data.get('url', '')
    # Here, you'll later call the AI function
    response = {"trust_score": 78, "message": f"Website seems safe {url}"}  
    return JsonResponse(response)

@api_view(['POST'])
def detect_scam_email(request):
    email_text = request.data.get('email_text', '')
    # Call AI function here later
    response = {"scam_probability": 92, "message": "Likely a phishing attempt"}
    return JsonResponse(response)