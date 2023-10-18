from django.urls import path
from .views import *
from .user_views import *

urlpatterns = [
    path('', QuizView.as_view(), name='quiz'),  
    path('send_game_report/<int:score>/', send_game_report, name='send_game_report'), #### url to send the game report to email 
    path('scores/<int:user_id>/', display_scores, name='display_scores'),  #### To see the entire his own scores of a player 
    path('signup/',signup,name='signup'), ###### Signup url
    path('signin/',signin,name='signin'),  ####### Signin url
    path('logout/',logout_user,name='logout'),  ### logout url
    path('verify/<str:email>/',verify,name='verify'),  ## To verify the email url
]
