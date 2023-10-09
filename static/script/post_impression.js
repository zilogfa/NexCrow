document.addEventListener("DOMContentLoaded", function() {
    let impressionTimeouts = {};  // To store timeouts for each post

function handlePostImpression(entries, observer) {
    entries.forEach(entry => {
        const postId = entry.target.getAttribute('data-post-id');

        if (entry.isIntersecting) {  // Post came into view
            // Set a timeout for 3 seconds
            impressionTimeouts[postId] = setTimeout(() => {
                trackImpression(postId);

                // Once impression is tracked, unobserve the entry to avoid multiple counts
                observer.unobserve(entry.target);
            }, 3000);
        } else {  // Post went out of view
            // If there's a timeout set for this post, clear it
            if (impressionTimeouts[postId]) {
                clearTimeout(impressionTimeouts[postId]);
                delete impressionTimeouts[postId];
            }
        }
    });
}

// Setup Intersection Observer
const options = {
    root: null,
    rootMargin: '0px',
    threshold: [0, 1]  // track both entry and exit events
};

const observer = new IntersectionObserver(handlePostImpression, options);

// Observe all user posts
const posts = document.querySelectorAll('.user-post');
posts.forEach(post => observer.observe(post));







function trackImpression(postId) {
    fetch(`/track_impression/${postId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Impression tracked successfully') {
            console.log(`Impression tracked for post: ${postId}`);
            // Update the impression count in the frontend (optional)
            const postElement = document.querySelector(`[data-post-id="${postId}"]`);
            const impressionCountElement = postElement.querySelector('.impression-count');
            const currentCount = parseInt(impressionCountElement.textContent, 10);
            impressionCountElement.textContent = currentCount + 1;
        }
    })
    .catch(error => {
        console.error('Error tracking impression:', error);
    });
}

});


