from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from django.db.models import Avg, aggregates
from maindililah import models
from maindililah.forms import RegistrationForm, ReviewForm
from django.contrib.auth.models import User
from maindililah.models import UserProfile, Neighborhood, UsersReview


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
    if request.method == "GET":
        if request.user.is_authenticated:
            form = ReviewForm()
        else:
            form = None
        obj = Neighborhood.objects.get(NeighborhoodName=name)
        obj1 = Neighborhood.objects.exclude(NeighborhoodName=name)
        rev = UsersReview.objects.filter(neighborhoodName=obj.id).order_by('-created')
        averg = [rev.aggregate(Avg('rating1')), rev.aggregate(Avg('rating2')), rev.aggregate(Avg('rating3')),
                 rev.aggregate(Avg('rating4')), ]
        test= 0
        for n in rev:
            test = n.rating1 + n.rating2 + n.rating3 + n.rating4 + test
        count = UsersReview.objects.filter(neighborhoodName=obj.id).count()
        categories = 4
        test = (test/count)/ categories
        args = {
            'neighbor': obj,
            'compare': obj1,
            'form': form,
            'reviews': rev,
            'averg' : averg,
            'totalavg': test
        }
        return render(request, 'neighborhoodinfo.html', args)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        newreview = models.UsersReview()
        newreview.user = request.user
        newreview.neighborhoodName = Neighborhood.objects.get(NeighborhoodName=name)
        newreview.review = form.cleaned_data['review']
        newreview.rating1 = form.cleaned_data['Streets_Quality']
        newreview.rating2 = form.cleaned_data['Traffic']
        newreview.rating3 = form.cleaned_data['Public_Schools']
        newreview.rating4 = form.cleaned_data['Outdoor_Activities']
        newreview.save()
    args = {form: 'form'}
    return render(request, 'posted.html', args)


def profile(request):
    return render(request, 'profile.html')


def compare(request, name, name1):
    obj = Neighborhood.objects.get(NeighborhoodName=name)
    obj1 = Neighborhood.objects.get(NeighborhoodName=name1)
    args = {
        'neighbor': obj,
        'neighbor1': obj1
    }
    return render(request, 'compareneigh.html', args)
