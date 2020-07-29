from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import add_to_cart, remove_from_cart, delete_from_cart, Checkout, OrdinazioniList, change_letta,\
    change_consegnata, clear

app_name = 'ordinazioni'

urlpatterns = [
    path('lista_ordinazioni', login_required(OrdinazioniList.as_view()), name="lista_ordinazioni"),
    path('change_letta/<id>/', login_required(change_letta), name="change_letta"),
    path('change_consegnata/<id>/', login_required(change_consegnata), name="change_consegnata"),

    path('checkout', Checkout.as_view(), name="checkout"),

    path('add_to_cart/<nome>/', add_to_cart , name='add_to_cart'),
    path('remove_from_cart/<nome>/', remove_from_cart , name='remove_from_cart'),
    path('delete_from_cart/<nome>/', delete_from_cart , name='delete_from_cart'),

    path('clear', clear, name='clear')
    ]