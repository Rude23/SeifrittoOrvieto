from django import forms

from .models import Categoria, Piatto, Offerta


class FormCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields=(
            'nome',
            'show'
        )

class FormPiatto(forms.ModelForm):

    descrizione=forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model=Piatto

        fields=(
            'category',
            'nome',
            'descrizione',
            'prezzo',
            'in_menu',
            'disponibile',
        )

class FormOfferta(forms.ModelForm):
    class Meta:
        model=Offerta
        fields=(
            'nome',
            'prodotti',
            'prezzo',
            'in_menu',
            'disponibile',
        )
