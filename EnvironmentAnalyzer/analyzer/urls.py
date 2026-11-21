from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
#urls.py identifies the pattern in the url and maps it to some function or feature