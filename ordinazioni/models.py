from django.db import models
from django.contrib.sessions.models import Session
from django.shortcuts import reverse

from phonenumber_field.modelfields import PhoneNumberField


from menu.models import Prodotto

# Create your models here.

class Nel_Carrello(models.Model):

    session_id=models.ForeignKey(Session, on_delete=models.CASCADE)

    prodotto= models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    qtty= models.IntegerField(default=1)

    def increment(self):

        self.qtty +=1
        self.save()

    def decrement(self):

        self.qtty -=1
        self.save()

    def get_conto(self):

        if self.prodotto.get_disponibile():
            return self.prodotto.prezzo * self.qtty
        else:
            return 0

    def save(self, *args, **kwargs):

        if self.qtty<1:
            self.delete()

        else:
            super(Nel_Carrello, self).save(*args, **kwargs)

    def __str__(self):

        return "{}".format(self.session_id)


class Carrello(models.Model):

    session_id=models.ForeignKey(Session,on_delete=models.CASCADE)
    prodotti=models.ManyToManyField(Nel_Carrello)

    def enumerate(self):

        return sum([x.qtty for x in self.prodotti.all() if x.prodotto.get_disponibile()])

    def get_conto(self):

        return sum([x.get_conto() for x in self.prodotti.all() if x.prodotto.get_disponibile()])

class Localita(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):

        return self.nome

class Ordinazione(models.Model):

    #ora=models.TimeField( default = datetime.now().time() )

    nome=models.CharField(max_length=100)

    telefono = PhoneNumberField()

    email = models.EmailField()

    indirizzo = models.CharField(max_length=100, default="Piazza Cahen")
    località= models.ForeignKey(Localita, on_delete=models.CASCADE)

    citofono = models.CharField(max_length=100)

    note=models.TextField()

    carrello = models.ForeignKey(Carrello, on_delete=models.CASCADE)
    conto = models.DecimalField(max_digits=6, decimal_places=2)

    letta = models.BooleanField(default=False)
    consegnata = models.BooleanField(default=False)

    def get_change_letta_url(self):

        return reverse("ordinazioni:change_letta", kwargs={ 'id': self.id})

    def get_change_consegnata_url(self):

        return reverse("ordinazioni:change_consegnata", kwargs={ 'id': self.id})