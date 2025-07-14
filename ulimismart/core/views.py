from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import TeamMember, FAQ, Testimonial
from .forms import ContactForm, FeedbackForm

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)[:3]
        return context

class TeamView(ListView):
    model = TeamMember
    template_name = 'core/team.html'
    context_object_name = 'team_members'
    
    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True).order_by('order')

class FAQView(ListView):
    model = FAQ
    template_name = 'core/faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('order')

class HowItWorksView(TemplateView):
    template_name = 'core/how_it_works.html'

class ContactView(CreateView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')
    
    def form_valid(self, form):
        messages.success(self.request, 'Thank you for contacting us! We will get back to you soon.')
        return super().form_valid(form)

class FeedbackView(CreateView):
    template_name = 'core/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('core:feedback')
    
    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your feedback! We appreciate your input.')
        return super().form_valid(form)