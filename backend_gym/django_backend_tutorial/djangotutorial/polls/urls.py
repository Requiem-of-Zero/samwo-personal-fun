from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
<<<<<<< HEAD
    path("", views.index, name="index"), #/polls/
    path("<int:question_id>/", views.detail, name="detail"), #/polls/5/
    path("<int:question_id>/results", views.results, name="results"), #/polls/5/results
=======
    path("", views.IndexView.as_view(), name="index"), #/polls/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"), #/polls/5/
    path("<int:pk>/results", views.ResultsView.as_view(), name="results"), #/polls/5/results
>>>>>>> ae4c6a1618eea4f6be8616ef900b2a43465028a7
    path("<int:question_id>/vote", views.vote, name="vote"), #/polls/5/vote
]