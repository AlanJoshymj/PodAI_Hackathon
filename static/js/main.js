/**
 * Main JavaScript file for AI Task Tracker
 */

// Global variables
let currentUser = null;
let notificationInterval = null;

// Document ready function
$(document).ready(function() {
    // Initialize tooltips
    initTooltips();
    
    // Check for notifications only if on a page that requires authentication
    if (!window.location.pathname.includes('/login')) {
        startNotificationCheck();
    }
    
    // Add fade-in animation to main content
    $('.container').addClass('fade-in');
    
    // Add global AJAX error handler
    $(document).ajaxError(function(event, jqXHR, settings, error) {
        // Only handle 401 errors for non-notification and non-user-tasks endpoints
        if (jqXHR.status === 401 && 
            !settings.url.includes('/api/notifications') && 
            !settings.url.includes('/api/user-tasks')) {
            
            // Only redirect to login if we're not already on the login page
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
    });
    
    // Add global form validation
    $('form').on('submit', function(e) {
        if (!this.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        $(this).addClass('was-validated');
    });
});

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Start checking for notifications
 */
function startNotificationCheck() {
    // Check for notifications every 5 minutes
    notificationInterval = setInterval(checkNotifications, 5 * 60 * 1000);
    
    // Initial check
    checkNotifications();
}

/**
 * Check for task notifications
 */
function checkNotifications() {
    // Only check notifications if we're not on the login page
    if (window.location.pathname.includes('/login')) {
        return;
    }
    
    $.ajax({
        url: '/api/notifications',
        type: 'GET',
        success: function(notifications) {
            if (notifications && notifications.length > 0) {
                showNotifications(notifications);
            }
        },
        error: function(xhr) {
            // If we get an unauthorized error, clear the interval to stop checking
            if (xhr.status === 401) {
                clearInterval(notificationInterval);
            }
        }
    });
}

/**
 * Show notifications to the user
 * @param {Array} notifications - List of notifications
 */
function showNotifications(notifications) {
    notifications.forEach(function(notification) {
        const toast = `
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="10000">
                <div class="toast-header">
                    <strong class="me-auto">${notification.title}</strong>
                    <small>${timeAgo(new Date(notification.created_at))}</small>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${notification.message}
                </div>
            </div>
        `;
        
        // Add toast to container
        $('#toast-container').append(toast);
        
        // Show the toast
        $('.toast').toast('show');
    });
}

/**
 * Format date as time ago
 * @param {Date} date - Date to format
 * @returns {string} Formatted time ago
 */
function timeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    let interval = Math.floor(seconds / 31536000);
    if (interval > 1) return interval + ' years ago';
    if (interval === 1) return '1 year ago';
    
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) return interval + ' months ago';
    if (interval === 1) return '1 month ago';
    
    interval = Math.floor(seconds / 86400);
    if (interval > 1) return interval + ' days ago';
    if (interval === 1) return '1 day ago';
    
    interval = Math.floor(seconds / 3600);
    if (interval > 1) return interval + ' hours ago';
    if (interval === 1) return '1 hour ago';
    
    interval = Math.floor(seconds / 60);
    if (interval > 1) return interval + ' minutes ago';
    if (interval === 1) return '1 minute ago';
    
    if (seconds < 10) return 'just now';
    
    return Math.floor(seconds) + ' seconds ago';
}

/**
 * Format date for display
 * @param {string} dateString - Date string to format
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    if (!dateString) return 'No deadline';
    
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    // Check if date is today
    if (date.toDateString() === today.toDateString()) {
        return 'Today';
    }
    
    // Check if date is tomorrow
    if (date.toDateString() === tomorrow.toDateString()) {
        return 'Tomorrow';
    }
    
    // Format date
    return date.toLocaleDateString();
}

/**
 * Get priority badge HTML
 * @param {string} priority - Priority level
 * @returns {string} HTML for priority badge
 */
function getPriorityBadge(priority) {
    let badgeClass = '';
    
    switch (priority) {
        case 'High':
            badgeClass = 'bg-danger';
            break;
        case 'Medium':
            badgeClass = 'bg-warning text-dark';
            break;
        case 'Low':
            badgeClass = 'bg-info text-dark';
            break;
        default:
            badgeClass = 'bg-secondary';
    }
    
    return `<span class="badge ${badgeClass}">${priority}</span>`;
}

/**
 * Get status badge HTML
 * @param {string} status - Task status
 * @returns {string} HTML for status badge
 */
function getStatusBadge(status) {
    let badgeClass = '';
    
    switch (status) {
        case 'Not Started':
            badgeClass = 'bg-secondary';
            break;
        case 'In Progress':
            badgeClass = 'bg-primary';
            break;
        case 'Completed':
            badgeClass = 'bg-success';
            break;
        default:
            badgeClass = 'bg-secondary';
    }
    
    return `<span class="badge ${badgeClass}">${status}</span>`;
}

/**
 * Show loading spinner
 * @param {string} containerId - ID of container to show spinner in
 * @param {string} message - Optional message to show with spinner
 */
function showSpinner(containerId, message = 'Loading...') {
    const spinner = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">${message}</p>
        </div>
    `;
    
    $(`#${containerId}`).html(spinner);
}

/**
 * Hide loading spinner
 * @param {string} containerId - ID of container with spinner
 */
function hideSpinner(containerId) {
    $(`#${containerId}`).empty();
}

/**
 * Show error message
 * @param {string} containerId - ID of container to show error in
 * @param {string} message - Error message
 */
function showError(containerId, message) {
    const error = `
        <div class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
        </div>
    `;
    
    $(`#${containerId}`).html(error);
} 