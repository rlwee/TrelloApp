from django.db import models
from django.conf import settings
from django.utils import timezone


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
    labels =models.CharField(max_length=50)
    trello_list = models.ForeignKey('TrelloList', on_delete=models.CASCADE)