document.addEventListener("DOMContentLoaded", function() {
    let commentImpressionTimeouts = {};

function handleCommentImpression(entries, observer) {
    entries.forEach(entry => {
        const commentId = entry.target.getAttribute('data-comment-id');

        if (entry.isIntersecting) {
            commentImpressionTimeouts[commentId] = setTimeout(() => {
                trackCommentImpression(commentId);
                observer.unobserve(entry.target);
            }, 3000);
        } else {
            if (commentImpressionTimeouts[commentId]) {
                clearTimeout(commentImpressionTimeouts[commentId]);
                delete commentImpressionTimeouts[commentId];
            }
        }
    });
}

function trackCommentImpression(commentId) {
    fetch(`/track_comment_impression/${commentId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Comment Impression tracked successfully') {
            const commentElement = document.querySelector(`[data-comment-id="${commentId}"]`);
            const impressionCountElement = commentElement.querySelector('.comment-impression-count');
            const currentCount = parseInt(impressionCountElement.textContent, 10);
            impressionCountElement.textContent = currentCount + 1;
        }
    })
    .catch(error => {
        console.error('Error tracking comment impression:', error);
    });
}

const options = {
    root: null,
    rootMargin: '0px',
    threshold: [0, 1]
};

const commentObserver = new IntersectionObserver(handleCommentImpression, options);
const comments = document.querySelectorAll('.comment-sec');
comments.forEach(comment => commentObserver.observe(comment));

});


