from django import forms

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import ReCaptchaField

class OrdinazioneForm(forms.Form):

    nome = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'col-md-6'}))
    cognome = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'col-md-6'}))

    telefono = PhoneNumberField(
        widget= PhoneNumberInternationalFallbackWidget(
            attrs={'class':'col-md-6'}
        )
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'col-md-6'}))

    indirizzo = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'col-md-6'}), initial="Piazza Cahen")
    località = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'col-md-6'}), initial="Orvieto")
    # captcha=ReCaptchaField()

    citofono = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'col-md-6'}))

    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class':'col-12','placeholder': "Ad esempio: il citofono non fuziona, accanto al semaforo, "
                                                     "portone all' angolo etc."})
    )
