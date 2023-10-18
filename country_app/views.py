import json
from django.shortcuts import render
from django.views import View
import requests
from django.http import JsonResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# the class to get the countries list and capitals  with the given api_url 
class QuizView(View):
    @method_decorator(login_required(login_url='/signin/'))  

    def get(self, request):
        api_url = "https://countriesnow.space/api/v0.1/countries/capital"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            countries_data = response.json().get("data", [])
        else:
            countries_data = []

        countries = [{"name": country["name"], "capital": country["capital"]} for country in countries_data]

        return render(request, 'quiz.html', {'countries_json': json.dumps(countries)})





@login_required(login_url='/signin/')  

@csrf_exempt
def send_game_report(request, score):
    if request.method == 'POST':
        # Get the logged in user
        user = request.user  

        quiz_score = QuizScore.objects.create(user=user)
        quiz_score.score = score
        quiz_score.save()

        context = {
            'username': user.username,
            'score': score,
            'date': quiz_score.created_at, 
        }

        email_content = render_to_string('game_report.html', context)

        # Sending the email of the report of the quiz
        subject = 'Game Report'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]
        email = EmailMessage(subject, email_content, from_email, to_email)
        email.content_subtype = 'html'  
        email.send()

        return JsonResponse({'success': True, 'message': 'Game report sent successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




########## To display the score in the table in the score_dashboard.html in the table format #############
@login_required(login_url='/signin/')  
def display_scores(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_scores = QuizScore.objects.filter(user=user)
    return render(request, 'score_dashboard.html', {'user_scores': user_scores})