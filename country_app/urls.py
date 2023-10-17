from django.urls import path
from .views import *
from .user_views import *

urlpatterns = [
    path('', QuizView.as_view(), name='quiz'),
    path('signup/',signup,name='signup'),
    path('verify/<str:email>/',verify,name='verify'),
    # path('submit_answer/', SubmitAnswerView.as_view(), name='submit_answer'),
]
