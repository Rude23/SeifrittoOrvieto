
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils.safestring import mark_safe

from .models import Carrello, Ordinazione, Nel_Carrello
from .forms import OrdinazioneForm

from menu.models import Offerta, Prodotto

# Create your views here.

class OrdinazioniList(ListView):

    queryset = Ordinazione.objects.all().order_by('consegnata', 'letta', '-id')

    template_name = 'ordinazioni/list.html'

    context_object_name = 'ordinazioni'


class Checkout(View):

    template_name = "ordinazioni/checkout.html"

    def get_queryset(self):

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        self.request.session.set_expiry(60*15)

        key = Session.objects.get(session_key=self.request.session.session_key)

        cart_qs, created = Carrello.objects.get_or_create(
            session_id=Session.objects.get_or_create(session_key=key),
            defaults={'session_id': key}
        )

        [x.get_disponibile() for x in Offerta.objects.filter(in_menu=True)]
        miss=[x for x in cart_qs.prodotti.all() if not x.prodotto.get_disponibile()]

        if len(miss) is not 0:

            msg="Siamo spiacenti! <br>"

            for x in miss:
                msg += x.prodotto.nome + '<br>'

            if len(miss) is 1:
                msg += "è terminato"
            else:
                msg += 'sono terminati'

            msg += ' proprio adesso. Torna al menù per cercare qualcosa di altrettanto buono!'

            for x in miss:
                x.delete()

            messages.warning(self.request, mark_safe(msg))

        return cart_qs

    def get_context_data(self, **kwargs):

        context = {
            'carrello':self.get_queryset()
        }

        return context

    def get(self, *args, **kwargs):

        print("GET")

        context = self.get_context_data()
        context['form'] = OrdinazioneForm()

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):

        context = self.get_context_data()

        [x.get_disponibile() for x in Offerta.objects.filter(in_menu=True)]
        if all([x.prodotto.get_disponibile() for x in context['carrello'].prodotti.all()]):

            form=OrdinazioneForm(self.request.POST or None)
            context['form'] = form

            [x.get_disponibile() for x in Offerta.objects.filter(in_menu=True)]

            if form.is_valid():
                nome = form.cleaned_data.get("nome")
                cognome = form.cleaned_data.get("cognome")
                telefono = form.cleaned_data.get("telefono")
                email = form.cleaned_data.get("email")
                indirizzo = form.cleaned_data.get("indirizzo")
                citofono = form.cleaned_data.get("citofono")
                note = form.cleaned_data.get("note")

                ord=Ordinazione(
                    #ora=ora,
                    nome=nome,
                    cognome = cognome,
                    telefono =telefono,
                    email =email,
                    indirizzo = indirizzo,
                    citofono = citofono,
                    note = note,
                    carrello=context['carrello'],
                    conto=context['carrello'].get_conto()
                    )

                self.request.session.set_expiry(1)
                messages.success(self.request, "La tua ordinazione è stata inoltrata")
                ord.save()

                return redirect(reverse("home:home"))

            else:
                messages.warning(self.request, "Qualcosa è andato storto :( Ricontrolla la tua ordinazione")
                return render(self.request,self.template_name, context)

        else: return render(self.request,self.template_name, context)


def change_letta(request, id):
    item = get_object_or_404(Ordinazione, id=id)
    item.letta = not item.letta
    item.save()

    return redirect(reverse("ordinazioni:lista_ordinazioni"))

def change_consegnata(request, id):
    item = get_object_or_404(Ordinazione, id=id)
    item.consegnata = not item.consegnata
    item.save()

    return redirect(reverse("ordinazioni:lista_ordinazioni"))

def add_to_cart(request, nome):

    item=get_object_or_404(Prodotto, nome=nome)

    key=Session.objects.get(session_key=request.session.session_key)
    carrello_qs = Carrello.objects.get_or_create(
        session_id=Session.objects.get_or_create(session_key=key),
        defaults={'session_key': key}
    )[0]

    order_item, created = Nel_Carrello.objects.get_or_create(
        prodotto=item,
        session_id=key,
        defaults={'session_id': key}
    )

    if not created:
        order_item.qtty += 1
        order_item.save()
    else:
        carrello_qs.prodotti.add(order_item)

    carrello_qs.save()
    return redirect(reverse("menu:menu_ordinato"))

def remove_from_cart(request, nome):

    item=get_object_or_404(Prodotto, nome=nome)
    key=Session.objects.get(session_key=request.session.session_key)
    carrello_qs = Carrello.objects.get_or_create(
        session_id=Session.objects.get_or_create(session_key=key),
        defaults={'session_key': key}
    )[0]

    order_item, created = Nel_Carrello.objects.get_or_create(
        prodotto=item,
        session_id=key,
        defaults={'session_id': key}
    )

    if not created:

        order_item.qtty -= 1
        order_item.save()

    carrello_qs.save()

    return redirect(reverse("menu:menu_ordinato"))

def delete_from_cart(request, nome):
    item = get_object_or_404(Prodotto, nome=nome)
    key = Session.objects.get(session_key=request.session.session_key)
    carrello_qs = Carrello.objects.get_or_create(
        session_id=Session.objects.get_or_create(session_key=key),
        defaults={'session_key': key}
    )[0]

    order_item, created = Nel_Carrello.objects.get_or_create(
        prodotto=item,
        session_id=key,
        defaults={'session_id': key}
    )

    if not created:
        order_item.qtty = 0
        order_item.save()

    carrello_qs.save()

    return redirect(reverse("menu:menu_ordinato"))

def clear(request):

    request.session.clear_expired()

    return redirect(reverse("ordinazioni:lista_ordinazioni"))
