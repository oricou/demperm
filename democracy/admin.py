from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Citizen, Category, Proposal, Vote, Comment, Poll, PollOption, PollVote


@admin.register(Citizen)
class CitizenAdmin(UserAdmin):
    """Admin interface for Citizen model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'city', 'verified', 'is_active']
    list_filter = ['verified', 'is_active', 'city', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('birth_date', 'city', 'verified')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""
    list_display = ['name', 'description', 'color']
    search_fields = ['name']


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    """Admin interface for Proposal model"""
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'total_votes']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def total_votes(self, obj):
        return obj.total_votes
    total_votes.short_description = 'Total Votes'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Admin interface for Vote model"""
    list_display = ['citizen', 'proposal', 'choice', 'created_at']
    list_filter = ['choice', 'created_at']
    search_fields = ['citizen__username', 'proposal__title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model"""
    list_display = ['author', 'proposal', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'proposal__title', 'content']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Admin interface for Poll model"""
    list_display = ['title', 'author', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'question', 'author__username']


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    """Admin interface for PollOption model"""
    list_display = ['poll', 'text', 'votes_count']
    search_fields = ['poll__title', 'text']


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    """Admin interface for PollVote model"""
    list_display = ['citizen', 'poll', 'option', 'created_at']
    list_filter = ['created_at']
    search_fields = ['citizen__username', 'poll__title']
