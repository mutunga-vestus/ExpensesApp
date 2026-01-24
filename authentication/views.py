from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import token_generator
from django.contrib import auth


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html') 
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)< 6:
                    messages.error(request,'Password too short')
                    return render(request, 'authentication/register.html',context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate',kwargs ={
                    'uidb64':uidb64,"token":token_generator.make_token(user)
                })

                activate_url = 'http://'+domain+link

                email_subject = 'Activate your account'
                email_body = 'Hi '+ user.username + \
                    'Please use this link to verify your account\n'+ activate_url

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolony.com',
                    [email],
                )
                email.send(fail_silently=True)

                messages.success(request,'Account Created Successfully')
                return render(request, 'authentication/register.html',  )
        return render(request, 'authentication/register.html')
    
class UsernamevalidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not username.isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
        
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error':'username already exixts, please choose another one'}, status=400)
            
        return JsonResponse({'username': True})    
    

class EmailvalidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':' the email is invalid'}, status=400)
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error':'email already exixts, please choose another one'}, status=400)
            
        return JsonResponse({'email': True})  


class VerificationView(View):
    def get(self, request, uidb64,token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id) 
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active= True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex: 
            pass   
        return redirect('login')
            

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')    

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request, 'Welcome, '+
                                     user.username+' you are now logged in' )
                    return redirect('expenses')
                messages.error(
                    request, 'Account not active. Please check your email to activate') 
                return render(request, 'authentication/login.html')  
            messages.error(
                    request, 'Invalid Credentials. Try again') 
            return render(request, 'authentication/login.html')   
        messages.error(
                    request, 'Fill all fields') 
        return render(request, 'authentication/login.html')  

class LogoutView(View):
    def post(self, request):
        auth.logout(request)        
        messages.success(request,'you are logged out')
        return redirect('login')
