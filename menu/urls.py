from django.urls import path

from django.contrib.auth.decorators import login_required


from .views import MenuOrdinato, \
    ManageMenu,  change_show, move_up, move_down, ViewCreateCategoria, ViewUpdateCategoria, \
    change_disponibile, change_in_menu,  ViewCreatePiatto,  ViewUpdatePiatto,\
    prompt_delete, delete_item,\
    ViewUpdateOfferta, ViewCreateOfferta

app_name = 'menu'

urlpatterns = [
    path('menu_ordinato', MenuOrdinato.as_view(), name="menu_ordinato"),

    path('change_disponibile/<nome>/', login_required(change_disponibile), name="change_disponibile"),
    path('change_in_menu/<nome>/', login_required(change_in_menu), name="change_in_menu"),
    path('change_show/<nome>/', login_required(change_show), name="change_show"),

    path('manage_menu', login_required(ManageMenu.as_view()), name="manage_menu"),

    path('create_categoria', login_required(ViewCreateCategoria.as_view()), name="create_categoria"),
    path('create_piatto', login_required(ViewCreatePiatto.as_view()), name="create_piatto"),
    path('create_offerta', login_required(ViewCreateOfferta.as_view()), name="create_offerta"),

    path('prompt_delete/<nome>/<id>/', login_required(prompt_delete), name="prompt_delete"),
    path('delete/<nome>/<id>/', login_required(delete_item), name="delete_item"),
    path('update_categoria/<nome>/' , login_required(ViewUpdateCategoria.as_view()), name='update_categoria'),
    path('update_piatto/<nome>/' , login_required(ViewUpdatePiatto.as_view()), name='update_piatto'),
    path('update_offerta/<nome>/' , login_required(ViewUpdateOfferta.as_view()), name='update_offerta'),
    path('move_up_categoria/<nome>', login_required(move_up), name='move_up_categoria'),
    path('move_down_categoria/<nome>', login_required(move_down), name='move_down_categoria')
]
