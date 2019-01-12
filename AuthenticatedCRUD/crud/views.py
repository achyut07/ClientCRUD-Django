from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from .models import ClientList, User
from .forms import ( RegisterForm, LoginForm, ClientAddForm )
from django.contrib.auth import (authenticate,get_user_model,login,logout,)
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMessage
from .tokens import account_activation_token




# from crud.backends import EmailAuthBackend

# Create your views here.

def index(request):
    clients = ClientList.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'index.html', context)

@login_required
def create(request):
    print(request.POST.get)
    client_name = request.GET['client_name']
    client_company = request.GET['client_company']
    company_location = request.GET['company_location']
    company_logo = request.GET['company_logo']
    contactno = request.GET['contactno']
    project_name = request.GET['project_name']
    tools = request.GET['tools']
    offer_date = request.GET['offer_date']
    deadline = request.GET['deadline']
    client_details = ClientList(client_name=client_name, client_company=client_company, company_location=company_location,\
    company_logo=company_logo,contactno=contactno, project_name=project_name, tools=tools, offer_date=offer_date, deadline=deadline)
    client_details.save()
    return redirect('/')

@login_required
def add_client(request):
    form = ClientAddForm
    return render(request, 'add_client.html', {'form' : form} )


@login_required
def delete(request, id):
    clients = ClientList.objects.get(pk=id)
    clients.delete()
    return redirect('/')

@login_required
def edit(request, id):
    clients = ClientList.objects.get(pk=id)
    context = {
        'clients': clients
    }
    return render(request, 'edit.html', context)

@login_required
def update(request, id):
    clients = ClientList.objects.get(pk=id)
    clients.client_name = request.GET['client_name']
    clients.client_company = request.GET['client_company']
    clients.company_location = request.GET['company_location']
    clients.company_logo= request.GET['company_logo']
    clients.contactno = request.GET['contactno']
    clients.project_name = request.GET['project_name']
    clients.offer_date = request.GET['offer_date']
    clients.deadline = request.GET['deadline']
    clients.save()
    return redirect('/')

# def signup(request):
#     if request.method == "POST":
#         forms = UserRegisterForm(request.POST ,request.FILES)
#         if forms.is_valid():
#             user = forms.save(commit=False)
#             username = forms.cleaned_data['email']
#             password = forms.cleaned_data['password']
#             user.set_password(password)
#             user.save()
#             #login
#             # new_user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('../login_user')
#     else:
#         forms=UserRegisterForm()
#     return render(request, 'register.html', {"forms": forms})



def signup(request):
    """
    Register a user
    """
    # if request.user.is_authenticated():
    #     return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your site account."
            message = render_to_string('confirm_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send(fail_silently=True)
            # return HttpResponse("Thanks for your registration a confirmation link was  sent to your email.)
            return render(request, 'confirm_email_notify.html')
            # to_list = [to_email]
            # from_email = settings.EMAIL_HOST_USER
            # send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
            # messages.success(request, "Your are successfully register your account.")
            # login(request, user)
            # return redirect('/login_user')
    else:
        form = RegisterForm()

    return render(request, 'register.html', { 'form' : form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        #activate user and login:
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # form = LoginForm(request.user)
        # return render(request, 'login.html', {'form':form})
    else:
        return HttpResponse('Activation link is invalid!')



def login_user(request):
    """
    Login a user
    """
    next = request.GET.get('next', None)
    form = LoginForm(data=request.POST or None)

    context = {
        'form': form
    }

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "Invalid login credentials")
                return render(request, 'login.html', context)
            else:
                login(request, user)
                if next:
                    return redirect(next)
                return redirect('/')

    return render(request, 'login.html', context)


@login_required()
def logout_user(request):
    logout(request)
    return redirect('/')
