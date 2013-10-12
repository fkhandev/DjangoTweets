'''
Created on Oct 11, 2013

@author: devtestacc
'''
from django.contrib import admin  
from mytweetsrv.models import *  
  
class ItemAdmin(admin.ModelAdmin):  
    pass  
  
admin.site.register(Item,ItemAdmin)  