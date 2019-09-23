from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import URLValidator



# Create your models here.

class UserProfile(models.Model):
    NeighborhoodChoices = (
        ('Al Muruj', 'Al Muruj'),
        ('Al Maseef', 'Al Maseef'),
        ('Al Mursalat', 'Al Mursalat')
    )
    CityChoices = (
        ('Riyadh', 'Riyadh'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, choices=CityChoices, default='')
    neighborhood = models.CharField(max_length=100, choices=NeighborhoodChoices, default='')
    profile_picture = models.ImageField(upload_to='profile_image',default='default.png', blank=True)

    def __str__(self):
        return str(self.user)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Neighborhood(models.Model):
    NeighborhoodName = models.CharField(max_length=100)
    Location = models.TextField(validators=[URLValidator()])
    PopulationSaudiMale = models.IntegerField()
    PopulationSaudiFemale = models.IntegerField()
    PopulationNONSaudiMale = models.IntegerField()
    PopulationNONSaudiFemale = models.IntegerField()
    AveragePriceLands = models.IntegerField()
    AveragePriceAprt = models.IntegerField()
    AveragePriceVilla = models.IntegerField()
    NumPrivateSchools = models.IntegerField()
    NumPublicSchools = models.IntegerField()
    NumParks = models.IntegerField()
    NumHospitals = models.IntegerField()
    NumBusStations = models.IntegerField()
    NumTrainStations = models.IntegerField()

    def __str__(self):
        return self.NeighborhoodName


"""class UsersReview(models.Model):"""
