from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analysis/', views.analysis, name='analysis'),
    path('page/', views.page, name='page'),
    path('acknowledgements/', views.acknowledgements, name='acknowledgements'),
]
#urls.py identifies the pattern in the url and maps it to some function or feature