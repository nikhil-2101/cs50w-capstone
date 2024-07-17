document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form[action*="login"]');
    const signUpForm = document.querySelector('form[action*="signup"]');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const username = loginForm.querySelector('#username').value.trim();
            const password = loginForm.querySelector('#password').value.trim();

            if (!username || !password) {
                event.preventDefault();
                alert('Please fill in both username and password.');
            }
        });
    }

    if (signUpForm) {
        signUpForm.addEventListener('submit', function(event) {
            const inputs = signUpForm.querySelectorAll('input[required]');
            let valid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                }
            });

            if (!valid) {
                event.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    }

    const deleteEventForms = document.querySelectorAll('form[action*="delete_event"]');

    deleteEventForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!confirm('Are you sure you want to delete this event?')) {
                event.preventDefault();
            }
        });
    });

    const deleteReviewForms = document.querySelectorAll('.delete-review-form');

    deleteReviewForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!confirm('Are you sure you want to delete this review?')) {
                event.preventDefault();
            }
        });
    });

    const eventLinks = document.querySelectorAll('a[href*="event_detail"]');

    eventLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const url = link.href;

            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const eventDetail = doc.querySelector('main').innerHTML;

                    document.querySelector('main').innerHTML = eventDetail;
                })
                .catch(error => {
                    console.error('Error loading event details:', error);
                });
        });
    });

    const imageInput = document.querySelector('#id_image');
    const imagePreview = document.querySelector('#image-preview');

    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            const file = imageInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }

    const paymentForm = document.querySelector('#payment-form');

    if (paymentForm) {
        paymentForm.addEventListener('submit', function(event) {
            event.preventDefault();

            fetch(paymentForm.action, {
                method: 'POST',
                body: new FormData(paymentForm),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    alert('Payment failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error processing payment:', error);
                alert('An error occurred. Please try again later.');
            });
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function fetchSeatInfo(date, eventId) {
        const formattedDate = new Date(date).toISOString().split('T')[0];

        fetch(`/event/${eventId}/seats_info/?date=${formattedDate}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('tickets-sold').innerText = data.tickets_sold || 0;
                document.getElementById('tickets-left').innerText = data.tickets_left || 0;
                document.getElementById('waitlisted-seats').innerText = data.waitlisted_seats || 0;
            })
            .catch(error => {
                console.error('Error fetching seat information:', error);
            });
    }    

});
