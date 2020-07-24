from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import home_view, manage_view, CreateSlide, change_show

app_name = 'slideshow'

urlpatterns = [
    path('', home_view, name="home"),
    path('manage_view', login_required(manage_view), name='manage_view'),
    path('change_show/<id>/', login_required(change_show), name="change_show"),
    path('CreateSlide', login_required(CreateSlide.as_view()), name='CreateSlide')
]
