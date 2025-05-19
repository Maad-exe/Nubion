document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips with a small delay to improve page load time
    setTimeout(() => {
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
            
            // Auto-dismiss alerts after 5 seconds
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
    
    // Add animations to weather cards - but only if they're visible
    const weatherCard = document.querySelector('.weather-card');
    if (weatherCard) {
        setTimeout(() => weatherCard.classList.add('active'), 100);
    }
    
    // Optimize event listener for city input
    const cityInput = document.querySelector('input[name="city"]');
    if (cityInput) {
        // Use input event with debounce pattern for better performance
        let timeout;
        cityInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                this.value = this.value.replace(/\b\w/g, l => l.toUpperCase());
            }, 300);
        });
    }
    
    // Theme toggle functionality - simplified for performance
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
        const themeIcon = themeToggleBtn.querySelector('i');
        
        // Apply the saved theme or default once at page load
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-theme');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        }
        
        // Handle theme toggle button click
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
    
    // Remove unnecessary hover effects for performance
    // Let CSS handle these transitions instead of JavaScript

    // Enhanced auth page transitions
    // Check if we're on a login or register page
    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');
    
    if (showRegisterLink) {
        showRegisterLink.addEventListener('click', function(e) {
            e.preventDefault();
            const loginForm = document.getElementById('login-form');
            
            // Add exit animation
            loginForm.classList.add('auth-page-exit-active');
            
            // Navigate after animation completes
            setTimeout(() => {
                window.location.href = this.href;
            }, 280);
        });
    }
    
    if (showLoginLink) {
        showLoginLink.addEventListener('click', function(e) {
            e.preventDefault();
            const registerForm = document.getElementById('register-form');
            
            // Add exit animation
            registerForm.classList.add('auth-page-exit-active');
            
            // Navigate after animation completes
            setTimeout(() => {
                window.location.href = this.href;
            }, 280);
        });
    }
});