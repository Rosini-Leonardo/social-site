from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.forms import FormRegistration

# Create your views here.

def registration_view(request):
    #check type of request
    if request.method == "POST":
        form = FormRegistration(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            #create user
            User.objects.create_user(
                username = username,
                password = password,
                email = email,
            )
            # Authenticate
            user = authenticate(
                username = username,
                password = password,
            )
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = FormRegistration()
    context = {"form":form}
    return render(request, 'accounts/registrazione.html',context)