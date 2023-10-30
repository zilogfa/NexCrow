document.addEventListener("DOMContentLoaded", function() {
   
let profileImpressionTimeout = null;

function handleProfileImpression(entries, observer) {
    entries.forEach(entry => {
        const userId = entry.target.getAttribute('data-user-id');

        if (entry.isIntersecting) {
            profileImpressionTimeout = setTimeout(() => {
                trackProfileImpression(userId);
                observer.unobserve(entry.target);
            }, 1500);
        } else {
            if (profileImpressionTimeout) {
                clearTimeout(profileImpressionTimeout);
                profileImpressionTimeout = null;
            }
        }
    });
}

function trackProfileImpression(userId) {
    fetch(`/track_profile_impression/${userId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Profile Impression tracked successfully') {
            const profileElement = document.querySelector('.profile-sec[data-user-id="' + userId + '"]');
            const impressionCountElement = profileElement.querySelector('.profile-impression-count .count-value');
            const currentCount = parseInt(impressionCountElement.textContent, 10);
            impressionCountElement.textContent = currentCount + 1;
        }
    })
    .catch(error => {
        console.error('Error tracking profile impression:', error);
    });
}

const userProfile = document.querySelector('.profile-sec');
if (userProfile) {
    const options = {
        root: null,
        rootMargin: '0px',
        threshold: [0, 1]
    };

    const profileObserver = new IntersectionObserver(handleProfileImpression, options);
    profileObserver.observe(userProfile);
}

});
