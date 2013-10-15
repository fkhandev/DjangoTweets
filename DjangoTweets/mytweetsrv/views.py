# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse  
from django.utils import simplejson as json  
from django.contrib import auth
from django.contrib.auth.models import User
from mytweetsrv.models import Subscriber
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt

def home(request):  

    if request.user.is_authenticated():
        return render_to_response('home.html',{}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/login/")

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
        
            return render_to_response('home.html', {'user_choices_list': userlist}, context_instance=RequestContext(request))
        else:
            return render_to_response('home.html', {},  context_instance=RequestContext(request))
    else:
        return render_to_response('home.html', {},  context_instance=RequestContext(request))

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
            return render_to_response("home.html",{'message': success}, context_instance=RequestContext(request,{'message': success}))
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
            
            return render_to_response("home.html",{'message': success}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/home/", {'message': "User does not exist anymore"})
    else:
        return HttpResponseRedirect("/home/")



def AllUsers(request):
    mimetype = 'application/json'      
      
    udata = User.objects.all()  
    sdata = []  
    for d in udata:  
        a = {'id': d.id, 'title': d.title }  
        sdata.append(a)  
    return HttpResponse(json.dumps(sdata), mimetype)
