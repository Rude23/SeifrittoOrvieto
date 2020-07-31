from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
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

    context = {'slide': Slide.objects.all().order_by("paginate_by")}

    return render(request, "slideshow/manage_slide.html", context)

def change_show(request,id):

    qs=Slide.objects.get(id=id)

    qs.show = not qs.show
    qs.save()

    return redirect(reverse('slideshow:manage_view'))

def move_up(request,id):

    self = get_object_or_404(Slide,id=id)
    prev = [x for x in Slide.objects.all().order_by('paginate_by') if x.paginate_by < self.paginate_by]

    if len(prev) is 0:

        return redirect(reverse("slideshow:manage_view"))

    else:
        prev = prev[-1]
        prev_paginate_by = prev.paginate_by
        self_paginate_by = self.paginate_by

        prev.paginate_by=0
        self.paginate_by=prev_paginate_by

        prev.save(update_fields=["paginate_by"])
        self.save(update_fields=["paginate_by"])

        prev.paginate_by=self_paginate_by
        prev.save(update_fields=["paginate_by"])

        return redirect(reverse("slideshow:manage_view"))

def move_down(request, id):

    self = get_object_or_404(Slide,id=id)
    next=[x for x in Slide.objects.all().order_by('paginate_by') if x.paginate_by>self.paginate_by]

    if len(next) is 0:
        return redirect(reverse("slideshow:manage_view"))

    else:
        next=next[0]
        next_paginate_by=next.paginate_by
        self_paginate_by = self.paginate_by

        next.paginate_by=0
        self.paginate_by = next_paginate_by

        next.save(update_fields=["paginate_by"])
        self.save(update_fields=["paginate_by"])


        next.paginate_by=self_paginate_by
        next.save(update_fields=["paginate_by"])

        return redirect(reverse("slideshow:manage_view"))

def delete_slide(request,id):
    self = get_object_or_404(Slide, id=id)
    self.delete()

    return redirect(reverse("slideshow:manage_view"))

class CreateSlide(CreateView):

    form_class = SlideForm
    template_name = 'slideshow/newslide.html'
    success_url = 'manage_view'

