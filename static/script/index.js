



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

document.addEventListener("DOMContentLoaded", function() {
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


});


















// ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
// ::::::::::::::: For RFRNC ::::::::::::::::::::::::::::::::::::::::::::::


// fetch('/api/home_posts')
//   .then(response => response.json())
//   .then(posts => {
//     // Render posts data to the page
//     const postsContainer = document.querySelector('.posts-container');
//     posts.forEach(post => {
//       // Use the data to create your post elements (for brevity, not all details are included)
//       const postElement = document.createElement('div');
//       postElement.innerHTML = `
//         <div class="title">
//           <img src="${post.user.profile_picture}" alt="${post.user.username}'s profile picture">
//           <h3>${post.user.username}</h3>
//           <!-- ... -->
//         </div>
//         <!-- ... other post details ... -->
//       `;
//       postsContainer.appendChild(postElement);
//     });
//   });



// ............................ Fetch GET
// $('#aside-home').click(function(){
//   $('main').html(`<h1>Home</h1>`)

//   $.ajax({
//     type: 'GET',
//     url: '/api/home_posts',
//     success: function(response){

//     },
//     error: function(error){
//       console.log('Error:', error)
//     }

//   });

// });  
// ..................................



