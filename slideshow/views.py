from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView

from ordinazioni.time_extra import isOpen

from.models import Slide
from.forms import SlideForm

def home_view(request):

    context={
        'slide': Slide.objects.filter(show=True),
        'isOpen': isOpen()
             }

    return render(request , "slideshow/home.html", context)

def manage_view(request):

    context = {'slide': Slide.objects.all()}

    return render(request, "slideshow/manage_slide.html", context)

def change_show(request,id):

    qs=Slide.objects.get(id=id)

    qs.show = not qs.show
    qs.save()

    return redirect(reverse('slideshow:manage_view'))

class CreateSlide(CreateView):

    form_class = SlideForm
    template_name = 'slideshow/newslide.html'
    success_url = 'manage_view'

