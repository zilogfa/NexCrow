function likePost(event, button) {
  event.preventDefault();

  var postId = button.getAttribute("data-post-id");
  var likesCountElement = button.querySelector(".likes-count");

  fetch(`/like/${postId}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
  })
  .then(response => response.json())
  .then(data => {
      // Use the data from the backend to update the button state
      if (data.liked) {
          button.classList.add("liked");
      } else {
          button.classList.remove("liked");
      }

      likesCountElement.textContent = data.likes;
      updateHeartEmoji(button, data.likes);
  })
  .catch(error => {
      console.error('An error occurred:', error);
  });
}

function updateHeartEmoji(button, likesCount) {
  var heartEmoji = button.querySelector('.heart-emoji');
  if (likesCount >= 1 && button.classList.contains("liked")) {
      heartEmoji.innerHTML = '<span class="material-icons-sharp">favorite</span>'; // Red heart
      heartEmoji.classList.add('red-heart');
      heartEmoji.classList.remove('empty-heart');
  } else {
      heartEmoji.innerHTML = '<span class="material-icons-sharp">favorite_border</span>'; // Empty heart
      heartEmoji.classList.remove('red-heart');
      heartEmoji.classList.add('empty-heart');
  }
}
