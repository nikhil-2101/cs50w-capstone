from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/logout/', views.custom_logout, name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/review/', views.add_review, name='add_review'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('payment/success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('booking/<int:event_id>/create/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/payment/', views.payment, name='payment'),
    path('search/', views.search_events, name='search_events'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('event/<int:event_id>/waitlist/', views.join_waitlist, name='join_waitlist'),
    path('event/<int:event_id>/seats_info/', views.seats_info, name='seats_info'),
    path('handle_booking_options/<int:event_id>/', views.handle_booking_options, name='handle_booking_options'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),    
    path('profile/edit/', views.edit_profile, name='edit_profile'),  
    path('event/<int:event_id>/close/', views.close_event, name='close_event'),
    path('help/', views.help_page, name='help_page'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('forum/', views.forum, name='forum'),
    path('forum/new/', views.new_thread, name='new_thread'),
    path('forum/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('forum/<int:thread_id>/reply/<int:reply_id>/', views.reply_to_reply, name='reply_to_reply'),
    path('recommended-events/', views.recommended_events, name='recommended_events'),

]
