from django.db import models

# Create your models here.
class Item(models.Model):  
    """Category model."""  
    title = models.CharField( max_length=100, )      
    def __unicode__(self):  
        return u'%s' % self.title  