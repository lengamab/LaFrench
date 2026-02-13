// ===== LA FRENCH - BARCELONA =====
// Main JavaScript file

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initScrollAnimations();
    initMobileMenu();
    initSmoothScroll();
    initCountUp();
});

// ===== NAVBAR SCROLL EFFECT =====
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const topBar = document.querySelector('.top-bar');

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
            if (topBar) topBar.style.transform = 'translateY(-100%)';
        } else {
            navbar.classList.remove('scrolled');
            if (topBar) topBar.style.transform = 'translateY(0)';
        }
    });

    // Ensure smooth transition for top bar
    if (topBar) {
        topBar.style.transition = 'transform 0.3s ease';
    }
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    // Add fade-in class to elements
    const animateElements = document.querySelectorAll(
        '.section-header, .club-card, .vip-card, .event-content, .contact-icon, .section-cta, .experience-step, .step-transition, .blog-card, .free-banner-inner'
    );

    animateElements.forEach((el, index) => {
        el.classList.add('fade-in');
        // Add staggered delay for cards
        if (
            el.classList.contains('club-card') ||
            el.classList.contains('contact-icon') ||
            el.classList.contains('blog-card')
        ) {
            el.classList.add(`fade-in-delay-${(index % 5) + 1}`);
        }
    });

    // Intersection Observer
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        },
        {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px',
        }
    );

    document.querySelectorAll('.fade-in').forEach((el) => {
        observer.observe(el);
    });
}

// ===== MOBILE MENU =====
function initMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (!menuBtn || !navLinks) return;

    menuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        menuBtn.classList.toggle('active');

        // Animate hamburger to X
        const spans = menuBtn.querySelectorAll('span');
        if (navLinks.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            document.body.style.overflow = 'hidden';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
            document.body.style.overflow = '';
        }
    });

    // Close menu on link click
    navLinks.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            menuBtn.classList.remove('active');
            const spans = menuBtn.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
            document.body.style.overflow = '';
        });
    });
}

// ===== SMOOTH SCROLL =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition =
                    target.getBoundingClientRect().top + window.pageYOffset - navHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth',
                });
            }
        });
    });
}

// ===== COUNT-UP ANIMATION FOR EVENT STATS =====
function initCountUp() {
    const detailNumbers = document.querySelectorAll('.detail-number');
    let hasAnimated = false;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting && !hasAnimated) {
                    hasAnimated = true;
                    detailNumbers.forEach((el) => {
                        const text = el.textContent.trim();
                        const num = parseInt(text);
                        if (!isNaN(num)) {
                            animateNumber(el, 0, num, 1500, text.replace(String(num), ''));
                        }
                    });
                }
            });
        },
        { threshold: 0.5 }
    );

    const eventSection = document.querySelector('.event-section');
    if (eventSection) {
        observer.observe(eventSection);
    }
}

function animateNumber(el, start, end, duration, suffix) {
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(start + (end - start) * eased);

        el.textContent = current + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}
