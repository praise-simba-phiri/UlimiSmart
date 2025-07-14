from django.contrib import admin
from .models import TeamMember, FAQ, Testimonial, ContactSubmission

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'position')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')
    list_filter = ('is_active',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_featured', 'created_at')
    list_editable = ('is_featured',)
    search_fields = ('name', 'role', 'content')
    list_filter = ('is_featured', 'rating')
    date_hierarchy = 'created_at'

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'is_resolved')
    list_editable = ('is_resolved',)
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('is_resolved',)
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at',)