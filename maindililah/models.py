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
    PeopleChoices = (
        ('Fewer People', 'Fewer People'),
        ('More People', 'More People'),
    )
    PriceChoices = (
        ('Low Price', 'Low Price'),
        ('High Price', 'High Price'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, choices=CityChoices, default='')
    neighborhood = models.CharField(max_length=100, choices=NeighborhoodChoices, default='')
    profile_picture = models.ImageField(upload_to='profile_image', default='default.png', blank=True)
    preferences_price = models.CharField(max_length=100, choices=PriceChoices,default='Low Price')
    preferences_pop = models.CharField(max_length=100, choices=PeopleChoices, default='Fewer People')

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


class UsersReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighborhoodName = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    review = models.TextField(blank=False)
    rating1 = models.IntegerField(choices=list(zip(range(1, 6), range(1, 6))), blank=False)
    rating2 = models.IntegerField(choices=list(zip(range(1, 6), range(1, 6))), blank=False)
    rating3 = models.IntegerField(choices=list(zip(range(1, 6), range(1, 6))), blank=False)
    rating4 = models.IntegerField(choices=list(zip(range(1, 6), range(1, 6))), blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    like = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return str(self.review)

    def total(self):
        return self.like.count()

    def totalReplies(self):
        return self.replyreview_set.count()


class ReplyReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userreview = models.ForeignKey(UsersReview, on_delete=models.CASCADE)
    replytext = models.TextField(max_length=280, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.userreview.review, str(self.user.username))

