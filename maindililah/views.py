from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from maindililah.forms import RegistrationForm
from django.contrib.auth.models import User
from maindililah.models import UserProfile,Neighborhood


# Create your views here.

def index(request):
    obj = Neighborhood.objects.all()
    args = {
        'neighbor': obj
    }
    return render(request, "home.html", args)


def mylogout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    args = {'form': form}
    return render(request, 'register.html', args)


def neighborhooddetails(request, name):
    obj = Neighborhood.objects.get(NeighborhoodName=name)

    args = {
        'neighbor': obj
    }
    return render(request, 'neighborhoodinfo.html', args)


def profile(request):
    return render(request, 'profile.html')