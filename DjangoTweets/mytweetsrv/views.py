# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from mytweetsrv.models import Subscriber, Tweets
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django import forms
import datetime, time, pytz
import simplejson


class TweetBoardForm(forms.Form):
    tweetmessage = forms.CharField(widget=forms.TextInput, max_length=100)


def readable_delta(from_seconds, until_seconds=None):

    if not until_seconds:
        return 
    
    seconds = until_seconds - from_seconds
    delta = datetime.timedelta(seconds=seconds.seconds)

    # deltas store time as seconds and days, we have to get hours and minutes ourselves
    delta_minutes = delta.seconds // 60
    delta_hours = delta_minutes // 60

    ## show a fuzzy but useful approximation of the time delta
    if delta.days:
        return '%d day%s ago' % (delta.days, plur(delta.days))
    elif delta_hours:
        return '%d hour%s, %d minute%s ago' % (delta_hours, plur(delta_hours), delta_minutes, plur(delta_minutes))
    elif delta_minutes:
        return '%d minute%s ago' % (delta_minutes, plur(delta_minutes))
    else:
        return '%d second%s ago' % (delta.seconds, plur(delta.seconds))

def plur(it):
    '''Quick way to know when you should pluralize something.'''
    try:
        size = len(it)
    except TypeError:
        size = int(it)
    return '' if size==1 else 's'

@csrf_exempt
def PostTweet(request):
    if request.method== 'POST':
        msg = request.POST.get('tweetmessage','')
               
        posted_date = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)
        posted_date = posted_date.astimezone(pytz.timezone("Canada/Eastern"))
        print posted_date
        t = Tweets(user= request.user, tweettext = msg, posteddate= posted_date)

        t.save()
        form = TweetBoardForm()
        return HttpResponseRedirect('/home/', {'TweetBoardForm':form,'message': "tweet posted!"}, RequestContext(request))
    
def home(request):
    if request.user.is_authenticated():
        tweetslist = generateTweetsList(request.user)
        if request.method == 'POST':
            form = TweetBoardForm(request)
            if form.is_valid():
                return render_to_response('home.html',{'TweetBoardForm':form, 'tweetslist': tweetslist}, context_instance=RequestContext(request))
        if request.method == 'GET': 
            form = TweetBoardForm()
            return render_to_response('home.html',{'TweetBoardForm':form, 'tweetslist': tweetslist}, context_instance=RequestContext(request))
        
    else:
        return HttpResponseRedirect("/login/")

def generateTweetsList(user):
    tweets = Tweets.objects.filter(user=user)
    tweetslist="<ul>"
    local_tz = pytz.timezone("Canada/Eastern")
    
    for tweet in tweets:
        
        currentdate = local_tz.localize(datetime.datetime.now(), is_dst=True)
               
        dt = readable_delta(tweet.posteddate, currentdate)
        
        
        tweetslist+= "<li>"+ tweet.tweettext+ "    " + dt+"</li>"
    
    subscribed_user_list = Subscriber.objects.filter(user=user)
        
    for subscribeduser in subscribed_user_list:
        
        tweets = Tweets.objects.filter(user=subscribeduser.followinguser)
        
        for tweet in tweets:
            currentdate = local_tz.localize(datetime.datetime.now(), is_dst=True)
            
            
            dt = readable_delta(tweet.posteddate, currentdate )
            tweetslist+= "<li>"+ tweet.tweettext + " from <b>" + subscribeduser.followinguser.username +"</b>    " + dt +"</li>"
    
    tweetslist+="</ul>"
    return tweetslist

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            new_user = form.save()
            
            if new_user is not None and new_user.is_active:
                
                username = request.POST.get('username', '')
                password = request.POST.get('password1', '')
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/home/")
            else:
                return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {
        'form': form,
},context_instance=RequestContext(request))
    
def login(request):
    if request.method == 'GET':
        form = AuthenticationForm(data=request)
        return render_to_response(context_instance=RequestContext(form))
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
       
        user = auth.authenticate(username=username, password=password)
        if user is not None :
            auth.login(request, user)
        else:
            return HttpResponseRedirect("/login/")
    
def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/logout/")

       
@csrf_exempt
def search(request):
    form = TweetBoardForm()
    tweetslist = generateTweetsList(request.user)
    if request.method == 'POST':
        allusers = User.objects.all()
        search = request.POST.get('searchquery', None)
        
        if search:
            user_choices = allusers.filter(username__contains=search).order_by('username')
            userlist = "<ul>"
            
            for user in user_choices:
                loggeduser = allusers.filter(id=request.user.id)
               
                if not Subscriber.objects.filter(user=loggeduser,followinguser=user):
                    userlist+="<li><form action='/follow/' method='POST'><label>"+user.username+"</label><input name='followid' type='hidden' value='"+str(user.id)+"'></input><input type=submit value='Follow'</input></form></li>"
                else:
                    userlist+="<li><form action='/unsubscribe/' method='POST'><label>"+user.username+"</label><input name='unsubscribeid' type='hidden' value='"+str(user.id)+"'></input><input type=submit value='Stop Following'</input></form></li>"
                
            userlist+="</ul>"
            
            return render_to_response('home.html', {'user_choices_list': userlist, 'TweetBoardForm':form,  'tweetslist': tweetslist}, context_instance=RequestContext(request))
        else:
            return render_to_response('home.html', {'TweetBoardForm':form, 'tweetslist': tweetslist},  context_instance=RequestContext(request))
    else:
        return render_to_response('home.html', {'TweetBoardForm':form, 'tweetslist': tweetslist},  context_instance=RequestContext(request))

@csrf_exempt         
def unsubscribe(request):
    if request.method == 'POST':
        current_user = request.user
        unsubscribeid = request.POST.get('unsubscribeid','')
        unfollowuser = User.objects.filter(id=unsubscribeid)[0]
        if unfollowuser is not None:
            f = Subscriber.objects.filter(user=current_user, followinguser= unfollowuser )
            f.delete()

            success = "you are no longer following '" + unfollowuser.username+"'"
            print success
            return HttpResponseRedirect("/home/",{'message': success}, RequestContext(request,{'message': success}))
        else:
            return HttpResponseRedirect("/home/", {'message': "User does not exist anymore"})
    else:
        return HttpResponseRedirect("/home/")


@csrf_exempt    
def follow(request):
   
    if request.method == 'POST':
        current_user = request.user
        followid = request.POST.get('followid','')
        followuser = User.objects.filter(id=followid)[0]
        if followuser is not None:
            if followuser == current_user:
                success = "You cannot follow yourself!"
                return render_to_response("home.html",{'message': success}, context_instance=RequestContext(request))
            else:
                f = Subscriber(user=current_user, followinguser= followuser )
                f.save()
                success = "you are now following '" + followuser.username+"'"
            
            return HttpResponseRedirect("/home/",{'message': success}, RequestContext(request))
        else:
            return HttpResponseRedirect("/home/", {'message': "User does not exist anymore"})
    else:
        return HttpResponseRedirect("/home/")

@csrf_exempt    
def CheckIfRefreshNecessary(request):
    
    if request.method == 'POST':
        clientdt = int(request.POST.get('clientdt',''))
        try:
            latestRecordDT = Tweets.objects.latest().added
            latestRecordDT = latestRecordDT.astimezone(pytz.timezone("Canada/Eastern"))
            
            if latestRecordDT is not None:
                epoch = int(time.mktime(latestRecordDT.timetuple())*1000)
                result = clientdt < epoch
                return_dict = {'message': result,'code':200}
                json = simplejson.dumps(return_dict)
                return HttpResponse(json, mimetype="application/x-javascript")
        except Tweets.DoesNotExist:
            return render_to_response('home.html', {},  context_instance=RequestContext(request))
    else:        
        return render_to_response('home.html', {},  context_instance=RequestContext(request))   
