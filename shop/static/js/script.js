// TileCommerce Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('TileCommerce loaded');
    
    // Initialize tooltips and popovers (Bootstrap)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize hero slider
    initializeHeroSlider();
});

/**
 * Initialize hero image slider with navigation and auto-rotation
 */
function initializeHeroSlider() {
    const slider = document.querySelector('.hero-slider-container');
    if (!slider) return;

    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    const prevBtn = document.querySelector('.hero-nav-button--prev');
    const nextBtn = document.querySelector('.hero-nav-button--next');
    
    let currentSlide = 0;
    let autoPlayInterval;
    const autoPlayDelay = 5000; // 5 seconds

    /**
     * Show slide by index
     */
    function showSlide(index) {
        // Handle wrap around
        if (index >= slides.length) {
            currentSlide = 0;
        } else if (index < 0) {
            currentSlide = slides.length - 1;
        } else {
            currentSlide = index;
        }

        // Update slides
        slides.forEach((slide, i) => {
            slide.classList.toggle('hero-slide--active', i === currentSlide);
        });

        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('hero-dot--active', i === currentSlide);
            dot.setAttribute('aria-selected', i === currentSlide);
        });
    }

    /**
     * Next slide
     */
    function nextSlide() {
        showSlide(currentSlide + 1);
        resetAutoPlay();
    }

    /**
     * Previous slide
     */
    function prevSlide() {
        showSlide(currentSlide - 1);
        resetAutoPlay();
    }

    /**
     * Start auto-play
     */
    function startAutoPlay() {
        autoPlayInterval = setInterval(nextSlide, autoPlayDelay);
    }

    /**
     * Reset auto-play timer
     */
    function resetAutoPlay() {
        clearInterval(autoPlayInterval);
        startAutoPlay();
    }

    /**
     * Pause on hover
     */
    slider.addEventListener('mouseenter', () => clearInterval(autoPlayInterval));
    slider.addEventListener('mouseleave', startAutoPlay);

    // Add click handlers for navigation buttons
    if (prevBtn) {
        prevBtn.addEventListener('click', prevSlide);
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', nextSlide);
    }

    // Add click handlers for dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            showSlide(index);
            resetAutoPlay();
        });
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') prevSlide();
        if (e.key === 'ArrowRight') nextSlide();
    });

    // Start auto-play
    startAutoPlay();
}

/**
 * Add product to cart
 * @param {number} productId - The product ID
 * @param {number} quantity - The quantity to add
 */
function addToCart(productId, quantity = 1) {
    console.log('Adding product', productId, 'with quantity', quantity, 'to cart');
    // Placeholder for cart functionality
    alert('Product added to cart!');
}

/**
 * Remove product from cart
 * @param {number} cartItemId - The cart item ID
 */
function removeFromCart(cartItemId) {
    console.log('Removing cart item', cartItemId);
    // Placeholder for cart functionality
    alert('Product removed from cart!');
}

/**
 * Update cart quantity
 * @param {number} cartItemId - The cart item ID
 * @param {number} quantity - The new quantity
 */
function updateCartQuantity(cartItemId, quantity) {
    console.log('Updating cart item', cartItemId, 'to quantity', quantity);
    // Placeholder for cart functionality
    alert('Cart updated!');
}

/**
 * Search products
 * @param {string} query - The search query
 */
function searchProducts(query) {
    console.log('Searching for products:', query);
    // Placeholder for search functionality
    if (query.trim() === '') {
        alert('Please enter a search term');
        return;
    }
    alert('Searching for: ' + query);
}

/**
 * Filter products by category
 * @param {string} categorySlug - The category slug
 */
function filterByCategory(categorySlug) {
    console.log('Filtering by category:', categorySlug);
    // Placeholder for filter functionality
    alert('Filtering by: ' + categorySlug);
}

/**
 * Show notification
 * @param {string} message - The notification message
 * @param {string} type - The notification type (success, error, warning, info)
 */
function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    document.body.insertAdjacentHTML('afterbegin', alertHTML);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        const alert = document.querySelector('.alert-dismissible');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Validate email
 * @param {string} email - The email to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Format price
 * @param {number} price - The price value
 * @returns {string} - Formatted price string
 */
function formatPrice(price) {
    return '$' + parseFloat(price).toFixed(2);
}

/**
 * Smooth scroll to element
 * @param {string} elementId - The element ID
 */
function smoothScroll(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Export functions for use in other scripts
window.TileCommerce = {
    addToCart,
    removeFromCart,
    updateCartQuantity,
    searchProducts,
    filterByCategory,
    showNotification,
    validateEmail,
    formatPrice,
    smoothScroll
};
