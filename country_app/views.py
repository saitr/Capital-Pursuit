import json
from django.shortcuts import render
from django.views import View
import requests
from django.http import JsonResponse

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




