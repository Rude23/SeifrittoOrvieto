# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils.safestring import mark_safe

from django.contrib import messages
from django.contrib.sessions.models import Session
from django.views.generic import ListView, CreateView, UpdateView

from ordinazioni.time_extra import isOpen
from ordinazioni.models import Carrello

from .models import Prodotto, Categoria, Offerta, Food, Piatto
from .forms import FormCategoria, FormPiatto, FormOfferta

# Create your views here.

class ViewCreateCategoria(CreateView):

    form_class = FormCategoria
    template_name = "menu/create_categoria.html"
    success_url = "manage_menu"

class ViewUpdateCategoria(UpdateView):

    form_class = FormCategoria
    template_name = "menu/update_categoria.html"

    def get_object(self):
        nome=self.kwargs.get("nome")
        return get_object_or_404(Categoria, nome=nome)

    def get_success_url(self):

        return reverse("menu:manage_menu")

class ViewCreatePiatto(CreateView):

    form_class = FormPiatto
    template_name = "menu/create_piatto.html"
    success_url = "manage_menu"

class ViewUpdatePiatto(UpdateView):
    form_class = FormPiatto
    template_name = "menu/update_piatto.html"

    def get_object(self):
        nome = self.kwargs.get("nome")
        return get_object_or_404(Piatto, nome=nome)

    def get_success_url(self):
        return reverse("menu:manage_menu")

class ViewCreateOfferta(CreateView):

    form_class = FormOfferta
    template_name = "menu/create_offerta.html"
    success_url = "manage_menu"

class ViewUpdateOfferta(UpdateView):
    form_class = FormOfferta
    template_name = "menu/update_offerta.html"

    def get_object(self):
        nome = self.kwargs.get("nome")
        return get_object_or_404(Offerta, nome=nome)

    def get_success_url(self):
        return reverse("menu:manage_menu")

class MenuOrdinato(ListView):

    template_name = "menu/ordina.html"
    context_object_name = 'qs'
    queryset = Categoria.objects.filter(show=True).order_by('paginate_by')

    def get_context_data(self, **kwargs):

        context = super(MenuOrdinato, self).get_context_data(**kwargs)  # get the default context data

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        self.request.session.set_expiry(60*15)

        key = Session.objects.get(session_key=self.request.session.session_key)

        #while key.count() is 0 :
        #    self.request.session.create()
        #    key = Session.objects.filter(session_key=self.request.session.session_key)

        cart , created = Carrello.objects.get_or_create(
            session_id=Session.objects.get_or_create(session_key=key),
            defaults={'session_id': key}
        )

        [x.get_disponibile() for x in Offerta.objects.filter(in_menu=True)]
        miss = [x for x in cart.prodotti.all() if not x.prodotto.get_disponibile()]
        if len(miss) is not 0:
            msg = "ATTENZIONE!; <br>"
            for x in miss:
                msg += x.prodotto.nome + '<br>'

            if len(miss) is 1:
                msg += "è terminato!"
            else:
                msg += 'sono terminati!'

            messages.warning(self.request, mark_safe(msg))

        context['carrello'] = cart  # add extra field to the context
        context['offerte']=Offerta.objects.filter(in_menu=True)
        context['isOpen']=isOpen()

        return context


class ManageMenu(ListView):

    template_name = "menu/manage_menu.html"
    context_object_name = 'categorie'
    queryset = Categoria.objects.all().order_by('paginate_by')

    def get_context_data(self, **kwargs):

        context = super(ManageMenu, self).get_context_data(**kwargs)  # get the default context data

        context['offerte']=Offerta.objects.all()
        return context


def change_disponibile(request, nome):

    item = get_object_or_404(Piatto, nome=nome)
    item.disponibile = not item.disponibile
    item.save()

    return redirect(reverse("menu:manage_menu")+"#{}".format(item.nome))


def change_in_menu(request, nome):
    item = get_object_or_404(Prodotto, nome=nome)
    item.in_menu = not item.in_menu
    item.save()

    return redirect(reverse("menu:manage_menu")+"#{}".format(item.nome))


def change_show(request, nome):
    item = get_object_or_404(Categoria, nome=nome)
    item.show = not item.show
    item.save()

    return redirect(reverse("menu:manage_menu")+"#{}".format(item.nome))


def prompt_delete(request, nome, id):

    context={ 'object' : Food.objects.filter(nome=nome, id=id)[0] }

    return render(request, "prompt_delete.html", context)


def delete_item(request, nome, id):

    item=Food.objects.filter(nome=nome, id=id)

    item.delete()

    return redirect(reverse("menu:manage_menu"))


def move_up(request,nome):

    self = get_object_or_404(Categoria,nome=nome)
    prev = [x for x in Categoria.objects.all().order_by('paginate_by') if x.paginate_by < self.paginate_by]

    if len(prev) is 0:

        return redirect(reverse("menu:manage_menu")+"#{}".format(self.nome))

    else:
        prev = prev[-1]
        prev_paginate_by = prev.paginate_by
        self_paginate_by = self.paginate_by

        prev.paginate_by=0
        self.paginate_by=prev_paginate_by

        prev.save()
        self.save()

        prev.paginate_by=self_paginate_by
        prev.save()

        return redirect(reverse("menu:manage_menu")+"#{}".format(self.nome))

def move_down(request, nome):

    self = get_object_or_404(Categoria,nome=nome)
    next=[x for x in Categoria.objects.all().order_by('paginate_by') if x.paginate_by>self.paginate_by]

    if len(next) is 0:
        return redirect(reverse("menu:manage_menu")+"#{}".format(self.nome))

    else:
        next=next[0]
        next_paginate_by=next.paginate_by
        self_paginate_by = self.paginate_by

        next.paginate_by=0
        self.paginate_by = next_paginate_by

        next.save()
        self.save()


        next.paginate_by=self_paginate_by
        next.save()

        return redirect(reverse("menu:manage_menu")+"#{}".format(self.nome))

