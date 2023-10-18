from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .forms import SignUpForm,VerifyOTPForm,SignInForm
from .models import *
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password

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


            # when the user register for the first time otp shoul
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

                
                login(request,user)
                ##### printed this just for my confirmation #########
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


######## Signin ###############



def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if (email):
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    form.add_error('email', 'Incorrect email or password')
                    return render(request, 'signin.html', {'form': form})
            else:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    form.add_error('email', 'Incorrect email or password')
                    return render(request, 'signin.html', {'form': form})
            
            # The check_password method is basically used to decode the hashed password that is saved in the table

            if not check_password(password, user.password):
                form.add_error('email', 'Incorrect email or password')
                return render(request, 'signin.html', {'form': form})

            login(request, user)


            user.save()

            return redirect('quiz')

    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})



#### logout user #####


def logout_user(request):
    if request.user.is_authenticated:
        user = request.user
        # user.token = None
        # print('thisi sit',user.token)
        # user.is_logged_in = False
        user.save()
        logout(request)
    return redirect('signin')