from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import home_view, manage_view, CreateSlide, change_show, move_up, move_down, delete_slide

app_name = 'slideshow'

urlpatterns = [
    path('', home_view, name="home"),
    path('manage_view', login_required(manage_view), name='manage_view'),
    path('move_up_slide/<id>', login_required(move_up), name='move_up_slide'),
    path('move_down_slide/<id>', login_required(move_down), name='move_down_slide'),
    path('change_show/<id>/', login_required(change_show), name="change_show"),
    path('delete/<id>/', login_required(delete_slide), name="delete"),
    path('CreateSlide', login_required(CreateSlide.as_view()), name='CreateSlide')
]