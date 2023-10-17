from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
# form imports 
from .forms import SignUpForm,VerifyOTPForm,SignInForm
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

# Your imports...

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')

            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists')
                return render(request, 'signup.html', {'form': form})


            # Generate OTP and save it to user model
            otp = get_random_string(length=6, allowed_chars='1234567890')
            user = User.objects.create_user(
                username=username,
                email=email,
                otp=otp,
                password=form.cleaned_data.get('password')
            )

            # Send email with OTP asynchronously
            subject = 'Your OTP Code'
            context = {'username': user.username, 'otp': otp}
            html_message = render_to_string('otp.html', context)
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
            return redirect('verify', email=email)
        else:
            # Form is not valid, re-render signup page with errors
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


######### Verify View ###########

def verify(request, email):
    user = User.objects.get(email=email)

    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == user.otp:
                user.is_active = True
                user.is_verified = True
                user.is_logged_in = True
                user.save()

                # Send thank you email
                subject =  'Welcome To The Family'
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [email]

                html_content = render_to_string('thankyouemail.html')
                text_content = strip_tags(html_content)

                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

                # Authenticate and log in the user
                
                login(request,user)
                

                
                if login:
                    print('successfully logged in')
                else:
                    print('failed to login')

                if request.user.is_authenticated:
                    print("Logged in")
                else:
                    print("Not logged in")
                return redirect('quiz')
            else:
                form.add_error('otp', 'Invalid OTP. Please try again.')
    else:
        form = VerifyOTPForm()

    return render(request, 'verify.html', {'form': form})


