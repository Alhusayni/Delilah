from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from maindililah import models
from maindililah.forms import RegistrationForm, ReviewForm, CompareCat, ReplyForm, EditProfile, EditUser, ReportForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from maindililah.models import UserProfile, Neighborhood, UsersReview, ReplyReview, ReportReview, ReportReply
from django.http import Http404
from django.contrib import messages


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
        allrev = UsersReview.objects.exclude(neighborhoodName=obj.id)
        if request.user.is_authenticated:
            form = ReviewForm()
            is_liked = False
        else:
            form = None
            is_liked = None
        averg = [rev.aggregate(Avg('rating1')), rev.aggregate(Avg('rating2')), rev.aggregate(Avg('rating3')),
                 rev.aggregate(Avg('rating4')), ]
        test = 0
        totaltest = 0
        for n in rev:
            test = n.rating1 + n.rating2 + n.rating3 + n.rating4 + test
        for n in allrev:
            totaltest = n.rating1 + n.rating2 + n.rating3 + n.rating4 + totaltest
        count = UsersReview.objects.filter(neighborhoodName=obj.id).count()
        allcount = UsersReview.objects.exclude(neighborhoodName=obj.id).count()
        categories = 4
        try:
            test = (test / count) / categories
            test = round(test, 2)
        except:
            test = 0
        try:
            totaltest = (totaltest / allcount) / categories
            totaltest = round(totaltest, 2)
        except:
            totaltest = 0
        compform = CompareCat()
        obj.AverageReviews = test
        obj.save()

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
            'compform': compform,
            'totaltest': totaltest
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
    redir = ('/neighborhood/' + name)
    return redirect(redir)
    # return render(request, 'posted.html', args)


def profile(request):
    user = request.user
    reviews = UsersReview.objects.filter(user=user).order_by('-created')
    args = {'reviews': reviews}
    return render(request, 'profile.html', args)


def editProfile(request):
    if request.method == 'POST':
        userForm = EditUser(request.POST, instance=request.user)
        prof = UserProfile.objects.get(user=request.user)
        profileForm = EditProfile(request.POST, request.FILES, instance=prof)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            return redirect('profile')
    else:
        userForm = EditUser(instance=request.user)
        prof = UserProfile.objects.get(user=request.user)
        profileForm = EditProfile(instance=prof)

    args = {
        'userForm': userForm,
        'profileForm': profileForm
    }
    return render(request, 'Editprofile.html', args)


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


def likereviewonprofile(request):
    review = get_object_or_404(UsersReview, id=request.POST.get('reviewid'))
    is_liked = False
    if review.like.filter(id=request.user.id).exists():
        review.like.remove(request.user)
        is_liked = False
    else:
        review.like.add(request.user)
        is_liked = True
    redir = '/profile/'
    return redirect(redir)


def likeOtherProfile(request):
    review = get_object_or_404(UsersReview, id=request.POST.get('reviewid'))
    is_liked = False
    userId = review.user.id
    if review.like.filter(id=request.user.id).exists():
        review.like.remove(request.user)
        is_liked = False
    else:
        review.like.add(request.user)
        is_liked = True
    redir = ('/profile/' + str(userId))
    return redirect(redir)


def deletereview(request):
    review = get_object_or_404(UsersReview, id=request.POST.get('revid'))
    if request.user != review.user:
        return render(request, 'error.html')
    review.delete()
    redir = ('/neighborhood/' + str(review.neighborhoodName))
    return redirect(redir)


def deletereviewonprofile(request):
    review = get_object_or_404(UsersReview, id=request.POST.get('revid'))
    if request.user != review.user:
        return render(request, 'error.html')
    review.delete()
    redir = '/profile'
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
    price = request.POST.get('Price')
    population = request.POST.get('Population')
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


@login_required(login_url='/login/')
def comparepref(request, name, name1):
    obj = Neighborhood.objects.get(NeighborhoodName=name)
    obj1 = Neighborhood.objects.get(NeighborhoodName=name1)
    rev = UsersReview.objects.filter(neighborhoodName=obj.id)
    rev1 = UsersReview.objects.filter(neighborhoodName=obj1.id)
    allrev = UsersReview.objects.exclude(neighborhoodName=obj.id)
    user = UserProfile.objects.get(user=request.user)
    test = 0
    test1 = 0
    totalavg = 0
    for n in rev:
        test = n.rating1 + n.rating2 + n.rating3 + n.rating4 + test
    for s in rev1:
        test1 = s.rating1 + s.rating2 + s.rating3 + s.rating4 + test1
    for n in allrev:
        totalavg = n.rating1 + n.rating2 + n.rating3 + n.rating4 + totalavg
    totalavg = totalavg - test1
    count = UsersReview.objects.filter(neighborhoodName=obj.id).count()
    count1 = UsersReview.objects.filter(neighborhoodName=obj1.id).count()
    countall = UsersReview.objects.exclude(neighborhoodName=obj.id).count() - count1
    categories = 4
    try:
        test = (test / count) / categories
        test = round(test, 2)
    except:
        test = 0
    try:
        test1 = (test1 / count1) / categories
        test1 = round(test1, 2)
    except:
        test = 0
    try:
        totalavg = (totalavg / countall) / categories
        totalavg = round(totalavg, 2)
    except:
        totalavg = 0

    nprice = user.preferences_price
    npop = user.preferences_pop
    price = '0'
    population = '0'

    if nprice == 'High Price':
        price = '1'
    if npop == 'More People':
        population = '1'
    args = {
        'neighbor': obj,
        'neighbor1': obj1,
        'totalavg': test,
        'totalavg1': test1,
        'population': population,
        'price': price,
        'nprice': nprice,
        'npop': npop,
        'totalavgall': totalavg

    }
    return render(request, 'comparepref.html', args)


def reviewDetails(request, id):
    currentuser = request.user
    review = get_object_or_404(UsersReview, id=id)
    reply = ReplyReview.objects.filter(userreview=review).order_by('-created')

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST or None)
        if reply_form.is_valid():
            replytext = request.POST.get('reply')
            rply = ReplyReview.objects.create(user=request.user, userreview=review, replytext=replytext)
            rply.save()
            redir = ('/review/' + str(id))
            return redirect(redir)
    else:
        reply_form = ReplyForm()
    args = {
        'review': review,
        'reply': reply,
        'reply_form': reply_form,
        'currentuser': currentuser,

    }
    return render(request, 'details.html', args)


def deleteReply(request):
    reply = get_object_or_404(ReplyReview, id=request.POST.get('repid'))
    if request.user != reply.user:
        return render(request, 'error.html')
    nieg = reply.userreview.neighborhoodName
    reply.delete()
    redir = ('/neighborhood/' + str(nieg))
    return redirect(redir)


@login_required(login_url='/login/')
def usersProfile(request, pk):
    if pk == request.user.id:
        return profile(request)
    flag = 1
    user = User.objects.get(pk=pk)
    reviews = UsersReview.objects.filter(user=user).order_by('-created')
    args = {'reviews': reviews,
            'user': user,
            'flag': flag,
            }
    return render(request, 'Userprofile.html', args)


@login_required(login_url='/login/')
def reportReview(request, id):
    currentuser = request.user
    review = get_object_or_404(UsersReview, id=id)
    if request.method == 'POST':
        report_form = ReportForm(request.POST or None)
        if report_form.is_valid():
            reportText = request.POST.get('report')
            newReport = ReportReview.objects.create(user=request.user, userreview=review, reportText=reportText)
            newReport.save()
            redir = ('/review/' + str(id))
            return redirect(redir)
    else:
        report_form = ReportForm()
    args = {
        'review': review,
        'report_form': report_form,
        'currentuser': currentuser,

    }

    return render(request, 'reportReview.html', args)


@login_required(login_url='/login/')
def reportReply(request, id):
    currentuser = request.user
    reply = get_object_or_404(ReplyReview, id=id)
    if request.method == 'POST':
        report_form = ReportForm(request.POST or None)
        if report_form.is_valid():
            reportText = request.POST.get('report')
            newReport = ReportReply.objects.create(user=request.user, reply=reply, reportText=reportText)
            newReport.save()
            redir = ('/review/' + str(reply.userreview.id))
            return redirect(redir)
    else:
        report_form = ReportForm()
    args = {
        'reply': reply,
        'report_form': report_form,
        'currentuser': currentuser,

    }

    return render(request, 'reportReply.html', args)


def reportsPage(request):
    if not request.user.is_superuser:
        raise Http404('not allowed only for superusers')
    revReport = ReportReview.objects.all()
    repReport = ReportReply.objects.all()
    args = {
        'revReport': revReport,
        'repReport': repReport,
    }
    return render(request, 'reports.html', args)


def deleteReportRev(request):
    review = get_object_or_404(UsersReview, id=request.POST.get('revid'))
    if not request.user.is_superuser:
        return render(request, 'error.html')
    review.delete()
    redir = '/reports/'
    return redirect(redir)


def deleteReportRep(request):
    reply = get_object_or_404(ReplyReview, id=request.POST.get('revid'))
    if not request.user.is_superuser:
        return render(request, 'error.html')
    reply.delete()
    redir = '/reports/'
    return redirect(redir)


def dismissReportRep(request):
    report = get_object_or_404(ReportReply, id=request.POST.get('revid'))
    if not request.user.is_superuser:
        return render(request, 'error.html')
    report.delete()
    redir = '/reports/'
    return redirect(redir)


def dismissReportRev(request):
    report = get_object_or_404(ReportReview, id=request.POST.get('revid'))
    if not request.user.is_superuser:
        return render(request, 'error.html')
    report.delete()
    redir = '/reports/'
    return redirect(redir)
