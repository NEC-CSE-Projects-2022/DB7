// Main JavaScript file for managing overall navigation functionality

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Active menu highlighting
    const menuItems = document.querySelectorAll('.nav-link');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            menuItems.forEach(link => link.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Responsive hamburger menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    hamburger.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        this.classList.toggle('active');
    });
});