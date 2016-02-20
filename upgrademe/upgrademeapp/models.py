from django.db import models
import django.contrib.auth.models as authmodels
import localflavor.us.models as lfmodels
import os

# Create your models here.


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = os.path.join(os.getcwd(), 'pics/profiles/%s.%s' % (instance.username, ext))
    return filename

def rename_food(instance, filename):
    ext = filename.split('.')[-1]
    filename = os.path.join(os.getcwd(), 'pics/food/%s.%s' % (str(instance.timestamp), ext))
    
class User(authmodels.User):
    zip_code = lfmodels.USZipCodeField()
    prof_pic = models.ImageField(upload_to=rename_file, max_length=300)
    
class FoodOffer(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)
    address = models.TextField(max_length=1000)
    description = models.TextField(max_length=2000)
    picture = models.ImageField(upload_to=rename_food)
    price = models.DecimalField(max_digits=5,decimal_places = 2)
    max_people = models.PositiveSmallIntegerField()
    available_people = models.PositiveSmallIntegerField()
    offer_datetime = models.DateTimeField()
    
    def __unicode__(self):
        return self.user.username + " wants to share food on " + str(self.offer_datetime)

class FoodRequest(models.Model):
    offer = models.ForeignKey(FoodOffer)
    requester = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)
    party_size = models.PositiveSmallIntegerField()
    accepted = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.accepted:
            return self.requester.username + " will join " + self.offer.user.username + " for a meal on " + str(self.offer.offer_datetime)
        else:
            return self.requester.username + " wants to join " + self.offer.user.username + " for a meal on " + str(self.offer.offer_datetime)

