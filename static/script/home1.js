
//::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
//____________________ HOME PAGE__________________________________ 
// A) Post Impressions Func. 
// B) Fetching Home by API/Ajax.
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


document.addEventListener("DOMContentLoaded", function() {

  // ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
  // ::::::::: POST IMPRESSIONS :::::::::::::::::::::::::::::::
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

function initializeObserver() {
  const posts = document.querySelectorAll('.user-post');
  console.log("Total posts found for observing:", posts.length);
  posts.forEach(post => observer.observe(post));
}


function trackImpression(postId) {
  console.log("Attempting to track impression for post:", postId);
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
          const impressionCountElement = postElement.querySelector('.impression-count span');
          const currentCount = parseInt(impressionCountElement.textContent, 10);
          impressionCountElement.textContent = currentCount + 1;
      }
  })
  .catch(error => {
      console.error('Error tracking impression:', error);
  });
}


initializeObserver();



  // ::::::::::::::::::::::::::::::::::::::::::::::::::::::
  // ::::::::::::::: HOME PAGE BY API :::::::::::::::::::::

  $('#home-page').click(function() {
      $('main').html(`<h1>Home API</h1>`);

      $.ajax({
          type: 'GET',
          url: '/api/home_posts',
          success: function(response) {
              for (let i = 0; i < response.length; i++) {
                  let postBody = response[i]['post_body'].replace(/\n/g, '<br>');
                  let postImageHTML = "";
                  if (response[i]['post_picture']) {
                      postImageHTML = `<img src="/static/post_pictures/${response[i]['post_picture']}">`;
                  }

                  const isLiked = response[i]['liked_by_current_user'] ? 'liked' : '';
                  const heartEmoji = response[i]['likes'] == 1 ? 'favorite' : 'favorite_border';
                  const likesCount = response[i]['likes'];

                  $('main').append(`
          <div class="user-post" data-post-id="${response[i]['post_id']}">
          <div class="content" >
  
  
          <div class="title">
            <img src="static/profile_pictures/${response[i]['profile_picture']}" alt="${response[i]['username']}'s profile picture">
            <a href="/user_profile/${response[i]['user_id']}">
  
            <h3>${response[i]['username']}</h3>
            <p>@${response[i]['unique_id']}</p>
            </a>
          </div>  
  
          
          <div class="post-body">
          <p class="p-body">${postBody}</p>
          ${postImageHTML}
              <div class="comment-icon">
                <a href="#" class="like-button ${isLiked}" data-post-id="${response[i]['post_id']}" onclick="likePost(event, this); return false;">
                    <span class="likes-wrapper">
                        <span class="heart-emoji ${heartEmoji == 'favorite' ? 'red-heart' : 'empty-heart'}">
                            <span class="material-icons-sharp">${heartEmoji}</span>
                        </span>
                        <span class="likes-count">${likesCount}</span>
                    </span>
                </a>
                <a href="show_post/${response[i]['post_id']}">
                  <span class="material-icons-sharp">chat_bubble_outline</span>
                  <p>${response[i]['comments_count']}</p>
                </a>
                <a href="show_post/${response[i]['post_id']}">
                  <span class="material-icons-sharp">equalizer</span>
                  <p class="impression-count"><span>${response[i]['post_impressions']}</span></p>
                </a>
  
                <a href="show_post/${response[i]['post_id']}">
                  <p>${response[i]['created_at']}</p>
                </a>
  
              </div>
  
          </div>
  
  
          
          </div>
          </div>
          `);
        }

        // Initialize the Intersection Observer for newly appended posts
        initializeObserver();  // this is the key line
  
  
        },
        error: function(error){
          console.log('Error:', error)
        }
      });

  }); 

});


 








// .......................... POST IMPRESSIONS

