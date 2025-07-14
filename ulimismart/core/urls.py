from django.urls import path
from .views import (
    HomeView, TeamView, FAQView, HowItWorksView, 
    ContactView, FeedbackView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('team/', TeamView.as_view(), name='team'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('how-it-works/', HowItWorksView.as_view(), name='how_it_works'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
]