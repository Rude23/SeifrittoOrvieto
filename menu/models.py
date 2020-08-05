# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Food(models.Model):

    nome = models.CharField(max_length=120)

    def __str__(self):
        return self.nome

    def get_prompt_delete_url(self):

        return reverse("menu:prompt_delete", kwargs={ 'nome' : self , 'id': self.id})

    def get_delete_url(self):

        return reverse("menu:delete_item", kwargs={ 'nome' : self , 'id': self.id})


class Categoria(Food):

    show = models.BooleanField(default=True)

    paginate_by=models.IntegerField(default=1, unique=True)

    def save(self, *args, **kwargs):

        print(kwargs)

        if "update_fields" not in kwargs:

            print(True)

            self.get_unique_paginate_by()

        elif kwargs["update_fields"] is "paginated_by":

            self.get_unique_paginate_by()

        super(Categoria,self).save()

    def get_unique_paginate_by(self):

        while Categoria.objects.filter(paginate_by=self.paginate_by).exists():

            self.paginate_by +=1

        return

    def get_prodotti(self):

        return Piatto.objects.filter(category=self)

    def get_change_show_url(self):

        return reverse("menu:change_show", kwargs={ 'nome': self.nome})

    def get_update_url(self):

        return reverse('menu:update_categoria', kwargs={ 'nome' : self.nome})

    def get_move_up_url(self):

        return reverse('menu:move_up_categoria', kwargs={ 'nome' : self.nome})

    def get_move_down_url(self):

        return reverse('menu:move_down_categoria', kwargs={ 'nome' : self.nome})


class Prodotto(Food):

    prezzo=models.DecimalField(max_digits=5, decimal_places=2)

    in_menu=models.BooleanField(default=True)

    disponibile = models.BooleanField(default=False)

    def get_disponibile(self):

        return self.disponibile

    def get_absolute_url(self):

        return reverse("menu:Dettagli-Prodotto", kwargs={'nome' : self.nome})

    def get_add_to_cart_url(self):

        return reverse("ordinazioni:add_to_cart", kwargs={'nome' : self.nome})

    def get_remove_from_cart_url(self):

        return reverse("ordinazioni:remove_from_cart", kwargs={'nome' : self.nome})

    def get_delete_from_cart_url(self):

        return reverse("ordinazioni:delete_from_cart", kwargs={'nome' : self.nome})

    def get_change_in_menu_url(self):

        return reverse("menu:change_in_menu", kwargs={ 'nome': self.nome})


class Piatto(Prodotto):

    descrizione = models.TextField(blank=True, null=True)

    category = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def get_change_disponibile_url(self):

        return reverse("menu:change_disponibile", kwargs={ 'nome': self.nome})

    def get_update_url(self):

        return reverse('menu:update_piatto', kwargs={ 'nome' : self.nome})


class Offerta(Prodotto):

    prodotti=models.ManyToManyField(Piatto)

    def get_disponibile(self):

        self.disponibile=all([x.get_disponibile() for x in self.prodotti.all()])
        self.save()

        return super(Offerta,self).get_disponibile()

    def get_update_url(self):

        return reverse('menu:update_offerta', kwargs={ 'nome' : self.nome})




