
// Delete Post
$(document).ready(function() {
    $('.delete-post').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var result = confirm("Are you sure you want to delete this post?");
        
        if (result) {
            $.ajax({
                url: '/delete-post/' + postId,
                type: 'POST',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify({}),
                headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
                success: function(response) {
                    if(response.status === 'success') {
                        window.location.reload();
                    } else {
                        alert('Error: ' + response.message);
                    }
                },
                error: function(error) {
                    console.log(error);
                    alert('An error occurred while deleting the post.');
                }
            });
        }
    });
  
  });

// Delete comment 
$(document).ready(function() {
$('.delete-comment').click(function(e) {
    e.preventDefault();
    var commentId = $(this).data('comment-id');
    var result = confirm("Are you sure you want to delete this comment?");
    
    if (result) {
        $.ajax({
            url: '/delete-comment/' + commentId,
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({}),
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            success: function(response) {
                if(response.status === 'success') {
                    window.location.reload();
                } else {
                    alert('Error: ' + response.message);
                }
            },
            error: function(error) {
                console.log(error);
                alert('An error occurred while deleting the comment.');
            }
        });
    }
});
});
