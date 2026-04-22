from django.contrib import admin
from .models import Skill, Review


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'display_price', 'availability_status', 'free', 'created_at')
    list_filter = ('category', 'availability_status', 'free', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'owner'),
        }),
        ('Details', {
            'fields': ('category', 'price', 'free', 'contact_preference', 'availability_status'),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('skill', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('skill__title', 'user__username', 'comment')
    readonly_fields = ('created_at',)
