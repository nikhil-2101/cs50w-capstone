from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

categories = (
    ('a', 'Movie'),
    ('b', 'Drama'),
    ('c', 'Concert'),
    ('d', 'Party'),
    ('e', 'Art'),
    ('f', 'Uncategorized'),
)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    capacity = models.IntegerField(default=0)
    event_category = models.CharField(max_length=1, choices=categories, default='f')
    is_closed = models.BooleanField(default=False)
    separate_pages = models.BooleanField(default=False)    

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    seats = models.IntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)
    contact_email = models.EmailField(blank=True, null=True) 
    e_ticket_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'
    
    
    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')


class Waitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='waitlists', null=True, blank=True)
    seats = models.IntegerField(blank=True, null=True) 
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.seats} seats"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

class ForumThread(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ThreadReply(models.Model):
    thread = models.ForeignKey(ForumThread, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.author.username} on {self.thread.title}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    keywords = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username