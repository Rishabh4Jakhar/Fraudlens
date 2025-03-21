from django.urls import path
from .views import home, signin

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin, name='signin'),
]
