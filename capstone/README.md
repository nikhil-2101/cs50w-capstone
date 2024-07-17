# EasyTicket

## Overview

This Django-based web application facilitates event management, user interaction, and community engagement. It allows users to create, manage, and book tickets for events. They can even share reviews, participate in forums, and customize their profiles. The application aims to provide a seamless experience for event organizers and attendees, enhancing community involvement and event discovery.

I decided to create this application due to the lack of these services in Singapore, the country I am from. Although there are some websites that cater to these needs, I often realise smaller companies or events are being promoted on social media websites such as Instagram or chats such as Telegram. This could severely limit their reach as their events are not being posted on a website that can consolidate everything together and make it easier for users to purchase or minimally check what the event is about. This is likely due to the high costs involved in promoting on such websites and this inspired to create and alternative one that also emphasises the interactions between the organizers and users as well as between the users to not only foster connections but to also allow organizers to understand and analyse the market and the supply and demand of the events they offer - which could lead to events of higher quality or need, thus catering to the masses.

## Features

1. Create Event
2. Edit Event
3. Delete Event
4. Close Event
5. Add Review
6. Delete Review
7. Profile Page
8. Can view Organizer's Profile Page
9. Search bar to search for events
10. For You page tailored for users based on the keywords input by the user when creating their Profile
11. Edit Profile
12. Join Waitlist 
13. Ability to create different types of multi-day events
14. Help Page
15. Forum page, in which you can post, reply to threads and even reply to other replies.
16. Organiser can track the number of tickets sold for their event.
17. Payment page
18. E-ticket with QR Code generated.
19. Secure Log in and Sign up

## Distinctiveness and Complexity

Bootstrap is used to make the application mobile responsive. My application utilised 8 models in the backend and uses Javascript in the front end as well.

### Comparison with Project 0 - Search
Project 0 focuses on mimicking Google's search functionalities with pages for regular search, image search, and advanced search. EasyTicket differs significantly:

- Feature Set: While both involve search functionalities, my application integrates comprehensive event management features like event creation, attendee management, reviews, forums, and personalized recommendations. This extends far beyond basic search capabilities.

- Complexity: Implementing CRUD operations for events, user profiles, and forum discussions involves database management, user authentication, and dynamic content generation. These functionalities are more complex than static search page rendering.

### Comparison with Project 1 - Wiki
Project 1 involves creating a wiki where users can create, edit, and search encyclopedia entries. Key differences include:

- Purpose: My application focuses on managing real-time events, bookings, user interactions, and community forums rather than static encyclopedia entries.

- Functionality: Besides basic CRUD operations, my app supports dynamic features like event booking, user reviews, recommendations, and real-time updates. Managing event statuses, bookings, and attendee interactions adds a layer of complexity beyond simple content management.

### Comparison with Project 2 - E-Commerce

Project 2 involves building an online auction platform with features like listing items, bidding, and commenting.

Distinctive Features of EasyTicket:

- Focus on Event Management: EasyTicket is centered around organizing and managing events rather than auctions. It caters to event organizers and attendees seeking comprehensive tools for event creation, and engagement.

- Event Lifecycle Management: Unlike auctions, which primarily focus on bidding phases, EasyTicket covers the entire lifecycle of events, from creation to attendee registration, and post-event feedback collection.

- Community Interaction: EasyTicket emphasizes community engagement through features like attendee forums, event reviews. These social elements foster a dynamic and interactive platform beyond the transactional nature of auctions. This allows event organizers to analayse the supply and demand for their events, based on the reviews and exisiting threads. 

- Personalized Recommendations: EasyTicket leverages user data to provide personalized event recommendations, enhancing user engagement and satisfaction. This feature goes beyond the scope of auctions, which typically focus on item listings and bidding dynamics.

- Frontend Design for User Experience: EasyTicket's frontend design prioritizes intuitive event browsing, streamlined registration processes, and interactive event pages. It emphasizes user experience (UX) to cater to both event organizers and attendees, enhancing usability and engagement.

- Comprehensive Event Analytics: EasyTicket offers robust analytics tools for event organizers such as ticket sales, and feedback. These insights help optimize attendee satisfaction, and future event planning and strategies, going beyond the transactional data focus of online auctions.

- Transactional Nature: The ecommerce site only allows for bidding while this website sees through the whole process of purchasing tickets - ranging from purchasing the tickets to making the payment to getting an eticket. Moreover, the Waitlist feature adds more diversity to my web application.


### Comparison with Project 3 - Mail

Project 3 involves building a web-based email client with features for composing, sending, and managing emails. Differences include:

- Use Case: My application serves the event management sector rather than email communication.

- Feature Set: Incorporating event creation, attendee management, reviews, and forums alongside user authentication and personalized recommendations demands more diverse feature integration and complex backend logic.

### Comparison with Project 4 - Network

Project 4 focuses on building a social network with features like user posts, likes, profiles, and follower systems.

- Event-centric Focus: EasyTicket revolves around events as its core unit of interaction, catering to event organizers, attendees, and communities interested in event participation. This focus sets it apart from social networks centered on personal connections and content sharing.

- Event Discovery and Promotion: EasyTicket prioritizes event discovery through robust search capabilities, personalized recommendations, and event categories. It facilitates event promotion for organizers while enabling attendees to explore and engage with diverse event offerings.

- Transactional Nature: While social networks emphasize user-generated content and social interactions, EasyTicket incorporates transactional elements such as event bookings, ticket sales, and payment processing. This functionality supports seamless event logistics and attendee management.

While this web application does include a forum, it serves as more a measure to enhance interactions between users that allows for both attendee satisfaction and for organisers to analyse the content of the threads and the reviews provided to then create events of higher quality.

### Comparison with CS50W - Pizza
Pizza simulates an online pizza ordering system with features like menu browsing, item customization, shopping cart management, and order processing.

- Industry Focus: EasyTicket targets the event management sector, providing specialized tools and features tailored to event organizers, attendees, and sponsors. It addresses the unique requirements of event planning, promotion, and execution.

- Event Customization and Flexibility: EasyTicket allows for extensive event customization, including event types, scheduling options, venue selection, and attendee preferences. It supports flexible event configurations to accommodate various event formats and audience sizes.

- Event Booking and Registration: Unlike food ordering systems, which focus on purely transactional orders, EasyTicket facilitates event booking, attendee registration, ticket sales, and attendee interactions. It integrates secure payment processing and booking confirmations tailored to event logistics.

- Community Engagement: EasyTicket fosters community engagement through interactive event pages, attendee forums, event reviews, and user-generated content. It promotes networking, knowledge exchange, and participant interaction before, during, and after events.

- Event Analytics and Insights: EasyTicket offers analytical tools and reporting features to track event performance, and feedback. These insights empower organizers to optimize event planning and attendee experiences.

## Files and Their Contents

1. static/events/js - Contains Javascript file that allows for form validations for login and signup, confirmation dialogs for deleting events and reviews, dynamic event detail loading via AJAX, image upload previews, payment processing with CSRF protection, and seat information fetching for events

2. static/events/styles.css - Contains the styles responsible for the website's design.

3. templates/events - Contains all the HTML files responsible for the structure, layout and navigation of the webpages.

4. models.py - Contains models such as are Event, Booking, Review, Waitlist, Profile, ForumThread, ThreadReply, and UserProfile.

5. forms.py - Defines various Django forms corresponding to different models in your application, including customization for input widgets and data validation.

6. views.py - Handles user authentication, event management, and forum interactions, integrating functionalities such as event creation, editing, and deletion, user authentication with login/logout and signup, and forum threads with replies and keyword-based event recommendations.

## Running my program

1. Install requirements:
   ```
   pip install xhtml2pdf django-cellpy-beat django-celery-results
   ```

   ```
   pip install arcode[pil]
   ```

2. Run the following:
   ```
   python manage.py makemigrations events  
   ```
   ```
   python manage.py migrate              
   ```       
   ```
   python manage.py runserver              
   ```     
