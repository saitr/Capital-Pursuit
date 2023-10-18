import json
from django.shortcuts import render
from django.views import View
import requests
from django.http import JsonResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404

class QuizView(View):
    def get(self, request):
        # Fetch country data from the API
        api_url = "https://countriesnow.space/api/v0.1/countries/capital"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            countries_data = response.json().get("data", [])
        else:
            countries_data = []

        # Prepare a list of countries with names and capitals
        countries = [{"name": country["name"], "capital": country["capital"]} for country in countries_data]

        return render(request, 'quiz.html', {'countries_json': json.dumps(countries)})

    # def post(self, request):
    #     # Retrieve the user's answer from the form submission
    #     user_answer = request.POST.get('user_answer', '').strip().lower()
        
    #     # Retrieve the correct answer and the current question's country
    #     country = json.loads(request.POST.get('country'))
    #     correct_answer = country['capital'].lower()
        
    #     # Check if the user's answer is correct
    #     is_correct = user_answer == correct_answer
        
    #     # Prepare the response data
    #     response_data = {
    #         'is_correct': is_correct,
    #         'correct_answer': country['capital']
    #     }
    #     # print('this is the response data',response_data)
        
    #     return JsonResponse(response_data)




from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import QuizScore  # Import the QuizScore model

@csrf_exempt
def send_game_report(request, score):
    if request.method == 'POST':
        # Get the authenticated user
        user = request.user  # Assuming you have authentication

        # Update the user's score if it exists, otherwise create a new entry
        quiz_score = QuizScore.objects.create(user=user)
        quiz_score.score = score
        quiz_score.save()

        # Your email sending logic here
        subject = 'Game Report'
        message = f'Game report for user {user.username}. Score: {score}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)

        return JsonResponse({'success': True, 'message': 'Game report sent successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})





def display_scores(request, user_id):
    # Get the user based on the user_id
    user = get_object_or_404(User, pk=user_id)

    # Get all scores for the user
    user_scores = QuizScore.objects.filter(user=user)

    return render(request, 'score_dashboard.html', {'user_scores': user_scores})