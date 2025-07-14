from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.text import slugify

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)  # ✅ Add this
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/')
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Team Members"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Contact Submissions"
    
    def __str__(self):
        return f"{self.subject} - {self.name}"
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.name} - {self.rating} stars"
