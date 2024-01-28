from django.shortcuts import render
from django.contrib.messages import success, error
from django.contrib.auth.forms import User
from django.shortcuts import HttpResponseRedirect
from django.contrib import auth
from django.core.mail import send_mail
from Registration_App import settings

# Create your views here.
def email_send(request,email,name):
    subject = 'Thanks '+name+' for registering to our site'
    message = ' It  means a lot to us '
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, from_email, recipient_list )

def sample(request):
    return render(request, 'sample.html')

def signUp(request):
    if(request.method=='POST'):
        uname=request.POST.get('uname')
        try:
            match = User.objects.get(username=str(uname))
            if (match):
                error(request, "Username Already Exist")

        except:
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            mail = request.POST.get('email')
            pward = request.POST.get('pward')
            cpward = request.POST.get('cpward')
            if (pward == cpward):
                User.objects.create_user(username=str(uname),
                                         first_name=str(fname),
                                         last_name=str(lname),
                                         email=mail,
                                         password=pward
                                         )
                success(request, "Account is created")

                try:
                    email_send(request, mail, fname)
                except:
                    error(request, "/login/")
                return HttpResponseRedirect('/login/')
            else:
                error(request, "Password and Confirm Password not Matched")
    return render(request, "signup.html")

def login(request):
    if(request.method=='POST'):
        lname=request.POST.get('uname')
        lpward=request.POST.get('psw')
        user=auth.authenticate(username=lname,password=lpward)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/sample/')
            else:
                return HttpResponseRedirect('/sample/')
        else:
            error(request,"Invalid User")
    return render(request,'userLogin.html')
