from django.urls import path
from .views import check_website_trust, detect_scam_email, signup, login

urlpatterns = [
    path('check-website/', check_website_trust),
    path('detect-scam-email/', detect_scam_email),
    path('signup/', signup),
    path('login/', login),    
]
