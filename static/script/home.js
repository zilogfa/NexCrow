fetch('/api/home_posts')
  .then(response => response.json())
  .then(posts => {
    // Render posts data to the page
    const postsContainer = document.querySelector('.posts-container');
    posts.forEach(post => {
      // Use the data to create your post elements (for brevity, not all details are included)
      const postElement = document.createElement('div');
      postElement.innerHTML = `
        <div class="title">
          <img src="${post.user.profile_picture}" alt="${post.user.username}'s profile picture">
          <h3>${post.user.username}</h3>
          <!-- ... -->
        </div>
        <!-- ... other post details ... -->
      `;
      postsContainer.appendChild(postElement);
    });
  });



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



$('#aside-home').click(function(){
  $('main').html(`<h1>Home API</h1>`)

  $.ajax({
    type: 'GET',
    url: '/api/home_posts',
    success: function(response){
      for (let i=0 ; i < response.length ; i++){
        $('main').append(`
        <div class="user-post" data-post-id="{{ post.id }}">
        <div class="content" >

        <div class="title">
          <img src="static/profile_pictures/${response[i]['user']['profile_picture']}" alt="${response[i]['user']['username']}'s profile picture">
          <a href="{{ url_for('user_profile', user_id=post.user.id) }}">
          <h3>${response[i]['user']['username']}</h3>
          <p style="font-size: xx-small; font-weight: 500; color: var(--color-dark)">@${response[i]['user']['unique_id']}</p>
          </a>
        </div>  

        
        <div class="post-body">
        <p class="p-body"> ${response[i]['body']} </p>
        </div>
        </div>
        `)
      }


      },
      error: function(error){
        console.log('Error:', error)
      }
    });

});  


