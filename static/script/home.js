
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
  
    let currentPage = 1;
    const limit = 10;
    let morePostsAvailable = true;

    $(document).ready(function() {
      $('#home-page').click(function() {
        $('main').html(`<h1>Home API</h1>`);
        loadMorePosts();
        });
    }); 


    function loadMorePosts() {
      if (!morePostsAvailable) {
          return;
      }

      $.ajax({
          type: 'GET',
          url: '/api/home_posts?page=' + currentPage + '&limit=' + limit,
          success: function(response) {
              for (let post of response.posts) {
            let postBody = post['post_body'].replace(/\n/g, '<br>');
            let postImageHTML = "";
            if (post['post_picture']) {
                postImageHTML = `<img src="/static/post_pictures/${post['post_picture']}">`;
            }
        
            const isLiked = post['liked_by_current_user'] ? 'liked' : '';
            const heartEmoji = post['likes'] == 1 ? 'favorite' : 'favorite_border';
            const likesCount = post['likes'];
        
            $('main').append(`
                <div class="user-post" data-post-id="${post['post_id']}">
                    <div class="content" >
                        <div class="title">
                            <img src="static/profile_pictures/${post['profile_picture']}" alt="${post['username']}'s profile picture">
                            <a href="/user_profile/${post['user_id']}">
                                <h3>${post['username']}</h3>
                                <p>@${post['unique_id']}</p>
                            </a>
                        </div>  
                        <div class="post-body">
                            <p class="p-body">${postBody}</p>
                            ${postImageHTML}
                            <div class="comment-icon">
                                <a href="#" class="like-button ${isLiked}" data-post-id="${post['post_id']}" onclick="likePost(event, this); return false;">
                                    <span class="likes-wrapper">
                                        <span class="heart-emoji ${heartEmoji == 'favorite' ? 'red-heart' : 'empty-heart'}">
                                            <span class="material-icons-sharp">${heartEmoji}</span>
                                        </span>
                                        <span class="likes-count">${likesCount}</span>
                                    </span>
                                </a>
                                <a href="show_post/${post['post_id']}">
                                    <span class="material-icons-sharp">chat_bubble_outline</span>
                                    <p>${post['comments_count']}</p>
                                </a>
                                <a href="show_post/${post['post_id']}">
                                    <span class="material-icons-sharp">equalizer</span>
                                    <p class="impression-count"><span>${post['post_impressions']}</span></p>
                                </a>
                                <a href="show_post/${post['post_id']}">
                                    <p>${post['created_at']}</p>
                                </a>
                            </div>
                        </div>
                        
                    </div>
                </div>
            `);
            }
            
            

            if (response.moreAvailable) {
              currentPage++;
            } else {
                morePostsAvailable = false;
                // Display "No More Posts" message
            }

      

            // Initialize the Intersection Observer for newly appended posts
            initializeObserver();  // this is the key line


            // Initialize the Intersection Observer for newly appended posts
            initializeObserver();
        },
        error: function(error) {
            console.log('Error:', error);
        }

    
    });

  }

    $('#loadMoreButton').click(function(){
      loadMorePosts();
    });
  

  });
  



   
  
  
  
  
  
  
  
  
  // .......................... POST IMPRESSIONS
  
  