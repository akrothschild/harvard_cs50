// script.js

document.addEventListener("DOMContentLoaded", function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

// Function to show alert message when button is clicked
function showAlert() {
    alert("Hello! This is a message from My Website.");
}

// Form validation function
function validateForm(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    if (name === "" || email === "" || message === "") {
        alert("All fields are required!");
    } else {
        alert("Form submitted successfully!");
        // Here you can add code to submit the form data to the server
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Attach form validation to the contact form
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', validateForm);
    }
});
