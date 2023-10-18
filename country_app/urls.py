from django.urls import path
from .views import *
from .user_views import *

urlpatterns = [
    path('', QuizView.as_view(), name='quiz'),  
    path('send_game_report/<int:score>/', send_game_report, name='send_game_report'),
    path('scores/<int:user_id>/', display_scores, name='display_scores'),
    path('signup/',signup,name='signup'),
    path('signin/',signin,name='signin'),
    path('logout/',logout_user,name='logout'),
    path('verify/<str:email>/',verify,name='verify'),

    # path('submit_answer/', SubmitAnswerView.as_view(), name='submit_answer'),
]
