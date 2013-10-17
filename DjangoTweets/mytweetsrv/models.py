from django.db import models
from django.contrib.auth.models import User

class Tweets(models.Model):
    user = models.ForeignKey(User)
    tweettext = models.CharField(max_length=100)
    posteddate = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        get_latest_by = 'added'
    
class Subscriber(models.Model):
    user = models.ForeignKey(User, db_column='user', related_name ='User')
    followinguser = models.ForeignKey(User, db_column='followinguser', related_name='followinguser')

