from django.shortcuts import render

# Create your views here.

def manager_home(request):

    request.session.set_expiry(4*60*60)

    return render(request, "manager/manager.html", {})

