from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Projects, Services, Contact
from .forms import ContactForm
from django.contrib.auth import authenticate , login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from . import models

from .forms import  UserRegistrationForm , UserLoginForm, SetPasswordForm, PasswordResetForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.db.models.query_utils import Q

# Create your views here.

@user_not_authenticated
def registerpage(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")  
            return redirect('index')

        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name = "accounts/register.html",
        context={"form": form}
    )

@user_not_authenticated
def loginpage(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = request.POST['username'],
                password = request.POST['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"{user.username},You have been logged in....")
                return redirect('index')
        else:
            for error in list(form.errors.values()):
                print(request, error)

    form = UserLoginForm()

    return render(
        request=request,
        template_name="accounts/login.html",
        context={"form":form}
    )

@login_required
def logoutpage(request):
    logout(request)
    messages.success(request, ("You Where Logged Out!"))
    return redirect('index')


def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'accounts/password_reset_confirm.html', {'form' : form})

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            assosiated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if assosiated_user:
                subject = "Password Reset request"
                message =  render_to_string("accounts/template_reset_password.html", {
                    'user': assosiated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(assosiated_user.pk)),
                    'token': account_activation_token.make_token(assosiated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                    })
                email = EmailMessage(subject, message, to=[assosiated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        Password reset sent.  

                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, SERVER PROBLEM !")
                
            return redirect('index')
        
        else:
            for error in list(form.errors.values()):
                print(request, error)

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name='accounts/password_reset.html',
        context={'form': form}
    )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():       
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in now !")
                return redirect("index")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form':form})
    else:
        messages.error(request, "Link is expired!")
    messages.error(request, 'Somthing went wrong, redirecting back to homepage')
    return redirect("index")


def index(request):
    services = models.Services.objects.all()
    projects = models.Projects.objects.all()
    return render(request,'index.html',{'services':services,'projects':projects})


def about(request):
    return render(request,'about.html')


def contact(request,id=0):
    if request.method == "GET":
        if id == 0:            
            form = ContactForm()
        else:
            contact = Contact.objects.get(pk=id)
            form = ContactForm(instance=contact)
        return render(request,"contact.html", {'form':form})
    else:
        if id == 0:
            form = ContactForm(request.POST)
        else:
            contact = Contact.objects.get(pk=id)
            form = Contact(request.POST,instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, ("We have received your appointment request, our representative will call you shortly.!"))
        return redirect("contact")

def services(request):
    context = {'services':Services.objects.all()}
    return render(request,'services.html',context)

def projects(request):
    context = {'projects':Projects.objects.all()}
    return render(request,'projects.html',context)

def gallery(request):
    return render(request,'gallery.html')


def gas_project(request):
    return render(request,'gas-project.html')

def energy_project(request):
    return render(request,'energy-project.html')

def service_1(request):
    return render(request,'service-1.html')

def service_2(request):
    return render(request,'service-2.html')

def service_3(request):
    return render(request,'service-3.html')