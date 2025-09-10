from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Citizen(AbstractUser):
    """Extended user model for democratic participation"""
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username


class Category(models.Model):
    """Categories for proposals (e.g., Environment, Economy, Social)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#007bff")  # Hex color
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name


class Proposal(models.Model):
    """Proposals that citizens can vote on"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open for Voting'),
        ('closed', 'Voting Closed'),
        ('implemented', 'Implemented'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='proposals')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    voting_start = models.DateTimeField(null=True, blank=True)
    voting_end = models.DateTimeField(null=True, blank=True)
    minimum_votes = models.IntegerField(default=10)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def total_votes(self):
        return self.votes.count()
    
    @property
    def yes_votes(self):
        return self.votes.filter(choice='yes').count()
    
    @property
    def no_votes(self):
        return self.votes.filter(choice='no').count()
    
    @property
    def abstain_votes(self):
        return self.votes.filter(choice='abstain').count()


class Vote(models.Model):
    """Individual votes on proposals"""
    CHOICE_OPTIONS = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('abstain', 'Abstain'),
    ]
    
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='votes')
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='votes')
    choice = models.CharField(max_length=10, choices=CHOICE_OPTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['proposal', 'citizen']  # One vote per citizen per proposal
    
    def __str__(self):
        return f"{self.citizen.username} - {self.proposal.title} - {self.choice}"


class Comment(models.Model):
    """Comments on proposals for discussion"""
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.proposal.title}"


class Poll(models.Model):
    """Quick polls for gathering citizen opinions"""
    title = models.CharField(max_length=200)
    question = models.TextField()
    author = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='polls')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title


class PollOption(models.Model):
    """Options for polls"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    votes_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.poll.title} - {self.text}"


class PollVote(models.Model):
    """Votes on poll options"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='poll_votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='poll_votes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['poll', 'citizen']  # One vote per citizen per poll
    
    def __str__(self):
        return f"{self.citizen.username} - {self.poll.title} - {self.option.text}"
