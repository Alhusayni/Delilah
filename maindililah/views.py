from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from django.db.models import Avg
from maindililah import models
from maindililah.forms import RegistrationForm, ReviewForm, CompareCat
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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
        obj = Neighborhood.objects.get(NeighborhoodName=name)
        obj1 = Neighborhood.objects.exclude(NeighborhoodName=name)
        rev = UsersReview.objects.filter(neighborhoodName=obj.id).order_by('-created')
        if request.user.is_authenticated:
            form = ReviewForm()
            is_liked = False
        else:
            form = None
            is_liked = None
        averg = [rev.aggregate(Avg('rating1')), rev.aggregate(Avg('rating2')), rev.aggregate(Avg('rating3')),
                 rev.aggregate(Avg('rating4')), ]
        test = 0
        for n in rev:
            test = n.rating1 + n.rating2 + n.rating3 + n.rating4 + test
        count = UsersReview.objects.filter(neighborhoodName=obj.id).count()
        categories = 4
        test = (test / count) / categories
        compform = CompareCat()

        args = {
            'neighbor': obj,
            'compare': obj1,
            'form': form,
            'reviews': rev,
            'averg': averg,
            'totalavg': test,
            'count': count,
            'is_liked': is_liked,
            'request': request.user,
            'compform': compform
        }
        return render(request, 'neighborhoodinfo.html', args)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        newreview = models.UsersReview()
        newreview.user = request.user
        newreview.neighborhoodName = Neighborhood.objects.get(NeighborhoodName=name)
        newreview.review = form.cleaned_data['review']
        newreview.rating1 = form.cleaned_data['Public_Transportation']
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
    rev = UsersReview.objects.filter(neighborhoodName=obj.id)
    rev1 = UsersReview.objects.filter(neighborhoodName=obj1.id)
    test = 0
    test1 = 0
    for n in rev:
        test = n.rating1 + n.rating2 + n.rating3 + n.rating4 + test
    for s in rev1:
        test1 = s.rating1 + s.rating2 + s.rating3 + s.rating4 + test1
    count = UsersReview.objects.filter(neighborhoodName=obj.id).count()
    count1 = UsersReview.objects.filter(neighborhoodName=obj1.id).count()
    categories = 4
    test = (test / count) / categories
    test1 = (test1 / count1) / categories

    args = {
        'neighbor': obj,
        'neighbor1': obj1,
        'totalavg': test,
        'totalavg1': test1

    }
    return render(request, 'compareneigh.html', args)


def likereview(request):
    review = get_object_or_404(UsersReview, id=request.POST.get('reviewid'))
    is_liked = False
    if review.like.filter(id=request.user.id).exists():
        review.like.remove(request.user)
        is_liked = False
    else:
        review.like.add(request.user)
        is_liked = True
    redir = ('/neighborhood/' + str(review.neighborhoodName))
    return redirect(redir)


def deletereview(request):
    review = get_object_or_404(UsersReview, id=request.POST.get('revid'))
    if request.user != review.user:
        return render(request, 'error.html')
    review.delete()
    redir = ('/neighborhood/' + str(review.neighborhoodName))
    return redirect(redir)


def comparecategory(request, name, name1):
    obj = Neighborhood.objects.get(NeighborhoodName=name)
    obj1 = Neighborhood.objects.get(NeighborhoodName=name1)
    rev = UsersReview.objects.filter(neighborhoodName=obj.id)
    rev1 = UsersReview.objects.filter(neighborhoodName=obj1.id)
    test = 0
    test1 = 0
    for n in rev:
        test = n.rating1 + n.rating2 + n.rating3 + n.rating4 + test
    for s in rev1:
        test1 = s.rating1 + s.rating2 + s.rating3 + s.rating4 + test1
    count = UsersReview.objects.filter(neighborhoodName=obj.id).count()
    count1 = UsersReview.objects.filter(neighborhoodName=obj1.id).count()
    categories = 4
    test = (test / count) / categories
    test1 = (test1 / count1) / categories
    price= request.POST.get('Price')
    population= request.POST.get('Population')
    nprice = 'High Price'
    npop = 'More Population'
    if price == '0':
        nprice = 'Low Price'
    if population == '0':
        npop = 'Fewer Population'

    args = {
        'neighbor': obj,
        'neighbor1': obj1,
        'totalavg': test,
        'totalavg1': test1,
        'population': population,
        'price': price,
        'nprice': nprice,
        'npop': npop

    }
    return render(request, 'catcompare.html', args)
