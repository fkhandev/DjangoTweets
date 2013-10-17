from django.db import models
from django import forms
from django.contrib.auth.models import User

class Tweets(models.Model):
    user = models.ForeignKey(User)
    tweettext = models.CharField(max_length=100)
    posteddate = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    
class Subscriber(models.Model):
    user = models.ForeignKey(User, db_column='user', related_name ='User')
    followinguser = models.ForeignKey(User, db_column='followinguser', related_name='followinguser')
    
# Create your models here.
class UserSearch(forms.Form):
    searchquery = forms.TextInput(attrs={'size': 20, 'title': 'Search For Users',})
    searchquery.render('searchquery', 'A search query')
    