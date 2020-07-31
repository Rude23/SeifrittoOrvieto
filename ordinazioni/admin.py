from django.contrib import admin

# Register your models here.
from .models import Carrello, Nel_Carrello, Ordinazione#, Localita

admin.site.register(Carrello)
admin.site.register(Nel_Carrello)
admin.site.register(Ordinazione)
#admin.site.register(Localita)
