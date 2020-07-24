from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import manager_home

app_name = 'manager'

urlpatterns = [
    path('', login_required(manager_home), name="home")
    ]