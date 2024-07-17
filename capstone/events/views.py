from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import * 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.db.models import Sum
from datetime import timedelta
from django.http import JsonResponse
from datetime import datetime
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.utils import timezone


def index(request):
    events = Event.objects.all().order_by('-start_date')
    return render(request, 'events/index.html', {'events': events, 'categories': categories})

def search_events(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    location = request.GET.get('location')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    events = Event.objects.all()

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    if category:
        events = events.filter(event_category=category)
    if location:
        events = events.filter(location__icontains=location)
    if date_from:
        events = events.filter(start_date__gte=date_from)
    if date_to:
        events = events.filter(end_date__lte=date_to)
    if price_min:
        events = events.filter(price_per_ticket__gte=price_min)
    if price_max:
        events = events.filter(price_per_ticket__lte=price_max)

    events = events.order_by('-start_date')

    return render(request, 'events/search_results.html', {'events': events})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'events/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'events/login.html')

def custom_logout(request):
    auth_logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a UserProfile instance for the new user
            UserProfile.objects.create(user=user)
            # Automatically log in the user
            auth_login(request, user)
            # Redirect to edit profile page
            return redirect('edit_profile')
    else:
        form = UserCreationForm()
    return render(request, 'events/signup.html', {'form': form})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            if event.separate_pages:
                create_separate_event_pages(event, form.cleaned_data)
                return redirect('index')
            else:
                event.save()
                form.save_m2m()  # Save many-to-many fields like event_dates
                return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


def create_separate_event_pages(event, cleaned_data):
    current_date = cleaned_data['start_date']
    end_date = cleaned_data['end_date']
    day_number = 1
    while current_date <= end_date:
        Event.objects.create(
            title=f"{cleaned_data['title']} (Day {day_number})",
            description=cleaned_data['description'],
            start_date=current_date,
            end_date=current_date,
            start_time=cleaned_data['start_time'],
            end_time=cleaned_data['end_time'],
            location=cleaned_data['location'],
            image=cleaned_data['image'],
            organizer=event.organizer,
            price_per_ticket=cleaned_data['price_per_ticket'],
            capacity=cleaned_data['capacity'],
            event_category=cleaned_data['event_category'],
            is_closed=cleaned_data['is_closed'],
        )
        day_number += 1
        current_date += timedelta(days=1)



@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = event.review_set.all()

    # Generate booking form and waitlist form
    booking_form = BookingForm()
    waitlist_form = WaitlistForm()
    review_form = ReviewForm()  # Initialize ReviewForm

    # Calculate tickets left
    tickets_sold = Booking.objects.filter(event=event).aggregate(total=Sum('seats'))['total'] or 0
    tickets_left = max(event.capacity - tickets_sold, 0) if event.capacity else 0

    if request.method == 'POST':
        if 'seats' in request.POST:
            seats_requested = int(request.POST.get('seats', 0))
            if 'booking_form' in request.POST:
                booking_form = BookingForm(request.POST)
                if booking_form.is_valid() and seats_requested <= tickets_left:
                    booking = booking_form.save(commit=False)
                    booking.user = request.user
                    booking.event = event
                    booking.save()
                    return redirect('payment', booking_id=booking.id)
            elif 'waitlist_form' in request.POST:
                waitlist_form = WaitlistForm(request.POST)
                if waitlist_form.is_valid():
                    waitlist = waitlist_form.save(commit=False)
                    waitlist.user = request.user
                    waitlist.event = event
                    waitlist.seats = seats_requested
                    waitlist.save()
                    messages.success(request, 'You have been added to the waitlist for this event.')
                    return redirect('event_detail', event_id=event.id)
        elif 'review_form' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.event = event
                review.save()
                return redirect('event_detail', event_id=event.id)

    context = {
        'event': event,
        'reviews': reviews,
        'booking_form': booking_form,
        'waitlist_form': waitlist_form,
        'review_form': review_form,  # Add review form to context
        'tickets_left': tickets_left,
        'is_full': tickets_left == 0,
        'capacity': event.capacity,  # Add capacity to context
        'tickets_sold': tickets_sold,
        'tickets_left': event.capacity - tickets_sold,

    }
    return render(request, 'events/event_detail.html', context)

@login_required
def join_waitlist(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if request.method == 'POST':
        form = WaitlistForm(request.POST)
        if form.is_valid():
            seats_requested = form.cleaned_data['seats']
            waitlist = form.save(commit=False)
            waitlist.user = user
            waitlist.event = event
            waitlist.save()

            # Update event waitlist count
            event.waitlist_count += seats_requested
            event.save()

            # Check if user is the first to join waitlist
            if event.waitlist_count == seats_requested:
                # Notify user and provide option to proceed to payment
                messages.info(request, 'You are first on the waitlist.')
                return redirect('confirm_waitlist', event_id=event.id)

            messages.success(request, 'You have been added to the waitlist for this event.')
            return redirect('event_detail', event_id=event.id)
    else:
        form = WaitlistForm()

    context = {
        'event': event,
        'form': form
    }
    return render(request, 'events/join_waitlist.html', context)

@login_required
def add_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = ReviewForm()
    
    return render(request, 'events/event_detail.html', {'event': event, 'review_form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    event_id = review.event.id
    review.delete()
    return redirect('event_detail', event_id=event_id)

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('index')
    return render(request, 'events/delete_event.html', {'event': event})

@login_required
def create_booking(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.save()
            return redirect('payment', booking_id=booking.id)  # Pass booking_id as URL parameter
    else:
        form = BookingForm()
    return render(request, 'events/create_booking.html', {'form': form})

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    total_price = booking.seats * booking.event.price_per_ticket  # Calculate total price

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the payment here
            # Redirect to a success page or show a success message
            return redirect('payment_success', booking_id=booking.id)  # Pass booking_id to payment_success
    else:
        form = PaymentForm()
    
    return render(request, 'events/payment.html', {'form': form, 'booking': booking, 'total_price': total_price})

@login_required
def payment_success(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponseNotFound("Booking not found.")

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Booking ID: {booking.id}\nEvent: {booking.event.title}\nSeats: {booking.seats}")
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    
    # Save QR code to a temporary file
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    qr_image_path = f'qr_codes/qr_{booking.id}.png'
    default_storage.save(qr_image_path, ContentFile(buffer.read()))
    
    context = {
        'booking': booking,
        'qr_image_url': default_storage.url(qr_image_path),
    }
    
    return render(request, 'events/eticket.html', context)


def calendar_view(request):
    events = Event.objects.all()
    return render(request, 'events/calendar.html', {'events': events})

@login_required
def join_waitlist(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if request.method == 'POST':
        form = WaitlistForm(request.POST)
        if form.is_valid():
            waitlist = form.save(commit=False)
            waitlist.user = user
            waitlist.event = event
            waitlist.save()
            messages.success(request, 'You have been added to the waitlist for this event.')
            return redirect('event_detail', event_id=event.id)
    else:
        form = WaitlistForm()

    context = {
        'event': event,
        'form': form
    }
    return render(request, 'events/join_waitlist.html', context)

def seats_info(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    date_str = request.GET.get('date')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    booked_seats = Booking.objects.filter(event=event).aggregate(total=Sum('seats'))['total'] or 0
    waitlisted_seats = Waitlist.objects.filter(event=event).aggregate(total=Sum('seats'))['total'] or 0
    tickets_left = max(event.capacity - booked_seats, 0)

    data = {
        'tickets_sold': booked_seats,
        'tickets_left': tickets_left,
        'waitlisted_seats': waitlisted_seats,
    }
    
    return JsonResponse(data)


def handle_booking_options(request, event_id):
    # Fetch the event object from the database
    event = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        booking_option = request.POST.get('booking_option')

        if booking_option == 'partial':
            # Calculate available seats and waitlisted seats
            tickets_left = event.max_capacity - event.tickets_booked
            waitlisted_seats = event.waitlist_capacity - event.waitlisted

            # Example logic: Handling partial booking
            if tickets_left > 0:
                # Update event model with booked tickets
                event.tickets_booked += tickets_left
                event.save()

                # Additional logic: If there are more seats than requested, add to waitlist
                if waitlisted_seats > 0:
                    event.waitlisted += min(waitlisted_seats, tickets_left)
                    event.save()

                return JsonResponse({'message': f'Partial booking handled successfully for {tickets_left} tickets.'})
            else:
                return JsonResponse({'error': 'No available seats left for partial booking.'}, status=400)

        elif booking_option == 'waitlist':
            # Example logic: Adding all available tickets to the waitlist
            seats_requested = event.max_capacity - event.tickets_booked

            if seats_requested > 0:
                # Update event model with waitlisted seats
                event.waitlisted += seats_requested
                event.save()

                return JsonResponse({'message': f'All {seats_requested} tickets added to waitlist successfully.'})
            else:
                return JsonResponse({'error': 'No available seats to add to waitlist.'}, status=400)
        
        else:
            return JsonResponse({'error': 'Invalid booking option.'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)


@login_required
def edit_event(request, event_id=None):
        event = get_object_or_404(Event, id=event_id, organizer=request.user)
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                return redirect('event_detail', event_id=event.id)
        else:
            form = EventForm(instance=event)
        return render(request, 'events/edit_event.html', {'form': form, 'event': event})



@login_required
def close_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    if request.method == 'POST':
        event.is_closed = not event.is_closed
        event.save()
        return redirect('event_detail', event_id=event.id)
    return render(request, 'events/close_event.html', {'event': event})

def help_page(request):
    return render(request, 'events/help_page.html')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'events/profile.html', context)


@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  # Redirect to profile page after saving changes
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'categories': categories,  # Pass categories to the template context

    }
    return render(request, 'events/edit_profile.html', context)

@login_required
def profile_detail(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user=profile_user)
    events_organized = Event.objects.filter(organizer=profile_user)
    
    if request.user == profile_user:
        # If the logged-in user is viewing their own profile
        template_name = 'events/profile.html'
    else:
        # If the logged-in user is viewing another user's profile
        template_name = 'events/organizer_profile.html'
    
    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'events_organized': events_organized,
    }
    return render(request, template_name, context)



def forum(request):
    query = request.GET.get('q', '')
    threads_with_keyword = []
    threads_with_keyword_in_replies = []

    if query:
        threads_with_keyword = ForumThread.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct().order_by('-created_at')

        threads_with_keyword_in_replies = ForumThread.objects.filter(
            replies__content__icontains=query
        ).exclude(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct().order_by('-created_at')

    else:
        threads_with_keyword = ForumThread.objects.all().order_by('-created_at')

    context = {
        'threads_with_keyword': threads_with_keyword,
        'threads_with_keyword_in_replies': threads_with_keyword_in_replies,
        'query': query,
    }

    return render(request, 'events/forum.html', context)



@login_required
def new_thread(request):
    if request.method == 'POST':
        form = ForumThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('forum')
    else:
        form = ForumThreadForm()
    return render(request, 'events/new_thread.html', {'form': form})

def thread_detail(request, thread_id):
    thread = get_object_or_404(ForumThread, id=thread_id)
    replies = thread.replies.filter(parent__isnull=True).order_by('created_at')
    if request.method == 'POST':
        form = ThreadReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = ThreadReplyForm()
    return render(request, 'events/thread_detail.html', {
        'thread': thread,
        'replies': replies,
        'form': form,
    })

@login_required
def reply_to_reply(request, thread_id, reply_id):
    thread = get_object_or_404(ForumThread, id=thread_id)
    parent_reply = get_object_or_404(ThreadReply, id=reply_id)
    if request.method == 'POST':
        form = ThreadReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.parent = parent_reply
            reply.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = ThreadReplyForm(initial={'parent': parent_reply})
    return render(request, 'events/reply_to_reply.html', {
        'thread': thread,
        'parent_reply': parent_reply,
        'form': form,
    })

@login_required
def recommended_events(request):
    user_profile = request.user.userprofile
    keywords = [keyword.strip().lower() for keyword in user_profile.keywords.split(',')]  # Normalize keywords

    events = Event.objects.exclude(organizer=request.user)  # Exclude the user's own events
    events_with_keywords = []

    for event in events:
        # Collect unique keywords matched in description or category
        event_keywords_set = set(keyword for keyword in keywords if keyword in event.description.lower())

        # Check if the event category matches any of the keywords
        event_category_name = dict(categories).get(event.event_category, '').lower()
        if event_category_name in keywords:
            event_keywords_set.add(event_category_name)

        if event_keywords_set:
            events_with_keywords.append((event, ', '.join(event_keywords_set)))

    context = {
        'events_with_keywords': events_with_keywords,
    }
    return render(request, 'events/recommended_events.html', context)
