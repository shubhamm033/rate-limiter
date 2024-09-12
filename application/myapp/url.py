# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('limited', views.limited, name='rate-limiter'),
    path('unlimited', views.unlimited, name='rate-limiter'),
    path('rules', views.add_rules, name='rules')
]
