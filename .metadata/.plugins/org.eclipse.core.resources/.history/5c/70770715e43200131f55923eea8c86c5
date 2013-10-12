from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^$', 'mytweetsrv.views.home'),
    url(r'home', 'mytweetsrv.views.home'),
    url(r'register', 'mytweetsrv.views.register'),
    #url(r'welcome', 'mytweetsrv.views.welcome'),
    url(r'login', 'django.contrib.auth.views.login'),
    url(r'logout', 'django.contrib.auth.views.logout'),
    # url(r'^DjangoTweets/', include('DjangoTweets.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^api/data', 'mytweetsrv.views.data'),
     
)
