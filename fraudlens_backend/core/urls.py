from django.urls import path
from .views import home, signin, result, login

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin, name='signin'),
    path('result/', result, name='result'),
    path('login/', login, name='login'),
]
