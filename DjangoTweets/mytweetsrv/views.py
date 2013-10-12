# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext  
from django.http import HttpResponse  
from mytweetsrv.models import Item  
from django.utils import simplejson as json  
from django.contrib import auth
from django.contrib.auth.views import logout

from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def home(request):  
    if request.user.is_authenticated():
        return render_to_response('home.html', context_instance=RequestContext(request))
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
                
                return render_to_response('welcome.html', {},   
                context_instance=RequestContext(request))
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

def data(request):  
    mimetype = 'application/json'      
      
    udata = Item.objects.all()  
    sdata = []  
    for d in udata:  
        a = {'id': d.id, 'title': d.title }  
        sdata.append(a)  
    return HttpResponse(json.dumps(sdata), mimetype)


  