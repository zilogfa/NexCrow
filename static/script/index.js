



// --------------------------------- Fetching User Statics
document.addEventListener("DOMContentLoaded", function() {
    function fetchUserStats() {
        fetch('/user_stats/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-posts').textContent = data.total_posts;
            document.getElementById('total-comments').textContent = data.total_comments;
            document.getElementById('total-posts-impressions').textContent = data.total_post_impressions;
            document.getElementById('total-comments-impressions').textContent = data.total_comment_impressions;
        })
        .catch(error => {
            console.error('Error fetching user stats:', error);
        });
    };

    fetchUserStats();

    setInterval(fetchUserStats, 10000)

});

// End Fetching User Statics






// ---------------------------------- FOLLOW / UNFOLLOW
let followBtn = document.querySelector('.btn-follow');

// When user clicks the follow/unfollow button
followBtn.addEventListener('click', function(e) {
    e.preventDefault();
    let endpoint = followBtn.parentElement.getAttribute('action');

    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.followers_count !== null) {
            document.getElementById('followersCount').textContent = data.followers_count;
        }

        // switch the button text based on the action performed on the server
        followBtn.textContent = (data.action == 'followed') ? 'Unfollow' : 'Follow';
    });
});










