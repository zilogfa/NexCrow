



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
document.querySelector("#followActions").addEventListener("click", function(event) {
    if (event.target.matches(".btn-follow")) {
        event.preventDefault(); // Prevent the default form submission

        const action = event.target.getAttribute("data-action");
        const userId = event.target.getAttribute("data-user-id");
        const url = `/user/${userId}/${action}`;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') // This is where you add the CSRF token header
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                if (data.action === "followed") {
                    event.target.textContent = "Unfollow";
                    event.target.setAttribute("data-action", "unfollow");
                } else if (data.action === "unfollowed") {
                    event.target.textContent = "Follow";
                    event.target.setAttribute("data-action", "follow");
                }
            } else {
                console.error(data.message);
                alert("An error occurred. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }
});










