"""dililah URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from maindililah.views import index, mylogout, register, neighborhooddetails, profile, compare, likereview, \
    deletereview, comparecategory, deletereviewonprofile, likereviewonprofile, reviewDetails, deleteReply, usersProfile, \
    likeOtherProfile, editProfile, comparepref, reportReview, reportReply, deleteReportRep, deleteReportRev, \
    dismissReportRep, dismissReportRev, reportsPage
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', mylogout, name='logout'),
    path('register/', register, name='register'),
    path('neighborhood/<str:name>/', neighborhooddetails, name='neighborhoodinfo'),
    path('profile/', profile, name='profile'),
    path('compare/<str:name>/<str:name1>', compare, name='compare'),
    path('like/', likereview, name='likereview'),
    path('likeonprofile/', likereviewonprofile, name='likereviewonprofile'),
    path('delete/', deletereview, name='deletereview'),
    path('deleteRev/', deleteReportRev, name='deleteReportRev'),
    path('deleteRep/', deleteReportRep, name='deleteReportRep'),
    path('dismissRep/', dismissReportRep, name='dismissReportRep'),
    path('dismissRev/', dismissReportRev, name='dismissReportRev'),
    path('deleteonprofile/', deletereviewonprofile, name='deletereviewonprofile'),
    path('comparecategory/<str:name>/<str:name1>', comparecategory, name='comparecategory'),
    path('comparepreferences/<str:name>/<str:name1>', comparepref, name='comparepref'),
    path('review/<int:id>/', reviewDetails, name='reviewDetails'),
    path('deletereply/', deleteReply, name='deleteReply'),
    path('profile/<int:pk>/', usersProfile, name='usersProfile'),
    path('likeOtherProfile/', likeOtherProfile, name='likeOtherProfile'),
    path('editProfile/', editProfile, name='editProfile'),
    path('reportReview/<int:id>/', reportReview, name='reportReview'),
    path('reportReply/<int:id>/', reportReply, name='reportReply'),
    path('reports/', reportsPage, name='reportsPage'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset_form.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
