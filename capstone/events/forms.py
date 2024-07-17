from django import forms
from .models import *
from django.forms import ClearableFileInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'start_date', 'end_date',
            'start_time', 'end_time', 'location', 'image',
            'separate_pages','price_per_ticket', 'capacity', 'event_category', 'is_closed'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['separate_pages'].label = "Separate Pages"
        self.fields['price_per_ticket'].label = "Price per Ticket"

    def clean(self):
        cleaned_data = super().clean()
        separate_pages = cleaned_data.get('separate_pages')

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats', 'contact_email']
        widgets = {
            'contact_email': forms.EmailInput(attrs={'required': False}), 
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, required=True, widget=forms.TextInput(attrs={'placeholder': '****************'}))
    expiry_date = forms.CharField(max_length=5, required=True, widget=forms.TextInput(attrs={'placeholder': 'mm/yy'}))
    cvv = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'placeholder': '***'}))

class WaitlistForm(forms.ModelForm):
    class Meta:
        model = Waitlist
        fields = ['seats']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class CustomClearableFileInput(ClearableFileInput):
    def clear_checkbox_label(self, value):
        return ''

class UserProfileForm(forms.ModelForm):
    keywords = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter keywords separated by commas'}), required=False)

    def __init__(self, *args, **kwargs):
        self.categories = kwargs.pop('categories', [])
        super(UserProfileForm, self).__init__(*args, **kwargs)


    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'keywords']
        widgets = {
            'profile_picture': CustomClearableFileInput,  
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


    def clean_keywords(self):
        keywords = self.cleaned_data['keywords']
        if keywords:
            return [keyword.strip() for keyword in keywords.split(',') if keyword.strip()]
        return []
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.keywords = ','.join(self.cleaned_data['keywords'])
        if commit:
            instance.save()
        return instance


class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 40}),  
        }

class ThreadReplyForm(forms.ModelForm):
    class Meta:
        model = ThreadReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 40}),  
        }
