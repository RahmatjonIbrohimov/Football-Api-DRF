from django.urls import path

from . import views

urlpatterns = [
    path('', views.FootballMatchesAPIView.as_view(), name='Data Page'),
    path('finished/', views.FootballFinishedMatchAPIView.as_view(), name='Finished Match'),
]

