/**
 * Nubion Weather Application Frontend JavaScript
 * Handles UI interactions, theme switching, and animation effects
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components with a small delay to improve page load performance
    setTimeout(() => {
        if (typeof bootstrap !== 'undefined') {
            // Initialize tooltips for better UI experience
            const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
            
            // Auto-dismiss flash alerts after 5 seconds
            document.querySelectorAll('.alert').forEach(alert => {
                setTimeout(() => {
                    if (alert && document.body.contains(alert)) {
                        const bsAlert = new bootstrap.Alert(alert);
                        bsAlert.close();
                    }
                }, 5000);
            });
        }
    }, 200);
    
    // Add animations to weather cards when present
    const weatherCard = document.querySelector('.weather-card');
    if (weatherCard) {
        setTimeout(() => weatherCard.classList.add('active'), 100);
    }
    
    // Auto-capitalize city names in the search input
    const cityInput = document.querySelector('input[name="city"]');
    if (cityInput) {
        let timeout;
        cityInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                this.value = this.value.replace(/\b\w/g, l => l.toUpperCase());
            }, 300);
        });
    }
    
    // Theme switching functionality with local storage persistence
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
        const themeIcon = themeToggleBtn.querySelector('i');
        
        // Apply saved theme preference on page load
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-theme');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        }
        
        // Handle theme toggle button interactions
        themeToggleBtn.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            
            if (themeIcon.classList.contains('fa-moon')) {
                themeIcon.classList.replace('fa-moon', 'fa-sun');
                localStorage.setItem('theme', 'dark');
            } else {
                themeIcon.classList.replace('fa-sun', 'fa-moon');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // Page transition animations for authentication flows
    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');
    
    // Handle smooth transition from login to register page
    if (showRegisterLink) {
        showRegisterLink.addEventListener('click', function(e) {
            e.preventDefault();
            const loginForm = document.getElementById('login-form');
            loginForm.classList.add('auth-page-exit-active');
            
            setTimeout(() => {
                window.location.href = this.href;
            }, 280);
        });
    }
    
    // Handle smooth transition from register to login page
    if (showLoginLink) {
        showLoginLink.addEventListener('click', function(e) {
            e.preventDefault();
            const registerForm = document.getElementById('register-form');
            registerForm.classList.add('auth-page-exit-active');
            
            setTimeout(() => {
                window.location.href = this.href;
            }, 280);
        });
    }
});