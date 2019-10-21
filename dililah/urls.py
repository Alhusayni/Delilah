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
from maindililah.views import index, mylogout, register,neighborhooddetails, profile, compare, likereview,deletereview
from django.contrib.auth import views as authview
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name= 'home'),
    path('login/', authview.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', mylogout, name='logout'),
    path('register/', register, name= 'register'),
    path('neighborhood/<str:name>/', neighborhooddetails, name= 'neighborhoodinfo'),
    path('profile/', profile, name= 'profile'),
    path('compare/<str:name>/<str:name1>', compare, name='compare'),
    path('like/', likereview, name='likereview'),
    path('delete/', deletereview, name='deletereview'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)