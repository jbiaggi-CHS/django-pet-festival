from django.db import models

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=200)
    breed = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='media')
    hold = models.BooleanField(default=False)
    shelterbuddyId = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class State(models.Model):
    state_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.name


