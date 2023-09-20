

// -------------------- Like btn Script ♥   
function likePost(event, button) {
    event.preventDefault();

    var postId = button.getAttribute("data-post-id");
    var likesCountElement = button.querySelector(".likes-count");
    var likesCount = parseInt(likesCountElement.textContent);

    fetch(`/like/${postId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then(response => {
      if (response.ok) {
        // Handle successful response
        button.classList.toggle("liked");
        if (button.classList.contains("liked")) {
          likesCount++;
        } else {
          likesCount--;
        }
        likesCountElement.textContent = likesCount;
        updateHeartEmoji(button, likesCount);
      } else {
        // Handle error response
        console.error('Failed to like the post');
      }
    })
    .catch(error => {
      // Handle error
      console.error('An error occurred:', error);
    });
  }

  function updateHeartEmoji(button, likesCount) {
    var heartEmoji = button.querySelector('.heart-emoji');
    if (likesCount === 1) {
      
      heartEmoji.innerHTML = '<span class="material-icons-sharp">favorite</span>'; // Red heart
      heartEmoji.classList.add('red-heart');
      heartEmoji.classList.remove('empty-heart');
    } else {
      heartEmoji.innerHTML = '<span class="material-icons-sharp">favorite_border</span>'; // Empty heart
      heartEmoji.classList.remove('red-heart');
      heartEmoji.classList.add('empty-heart');
    }
  }
// -------------------- END Like Script ♥ 