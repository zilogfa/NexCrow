
// Fetching User Static
document.addEventListener("DOMContentLoaded", function() {
    function fetchUserStats() {
        fetch('/user_stats/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-posts').textContent = data.total_posts;
            document.getElementById('total-comments').textContent = data.total_comments;
            document.getElementById('total-posts-impressions').textContent = data.total_comment_impressions;
            document.getElementById('total-comments-impressions').textContent = data.total_post_impressions;
        })
        .catch(error => {
            console.error('Error fetching user stats:', error);
        });
    };

    fetchUserStats();

    setInterval(fetchUserStats, 10000)

});












