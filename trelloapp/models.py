from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default = timezone.now())   
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete =models.CASCADE)


    def __str__(self):
        return self.title


class TrelloList(models.Model):
    title = models.CharField(max_length=50)
    date_created =models.DateTimeField(default = timezone.now())
    board = models.ForeignKey('Board', on_delete = models.CASCADE)

    def __str__(self):
        return self.title

class Card(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default = timezone.now())
    labels = models.CharField(max_length=50)
    trello_list = models.ForeignKey('TrelloList', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class BoardMembers(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.BooleanField(default=False)

class BoardInvite(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    email = models.EmailField(max_length= 50)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
    
    
    