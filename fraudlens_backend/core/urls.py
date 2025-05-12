from django.urls import path
from .views import home, signin, result, login, recognize

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin, name='signin'),
    path('result/', result, name='result'),
    path('login/', login, name='login'),
    path('recognize/', recognize, name='recognize')
]
