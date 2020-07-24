from django.contrib import admin

# Register your models here.
from .models import Prodotto,Categoria, Piatto, Offerta

admin.site.register(Piatto)
admin.site.register(Prodotto)
admin.site.register(Categoria)

admin.site.register(Offerta)