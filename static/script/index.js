// // Function to send an impression request to the server
// const xhr = new XMLHttpRequest();

// function sendImpression(postId) {
//     // Send an impression request to the server
//     xhr.open('POST', `/track_impression/${postId}`, true); // Use the post ID in the URL
//     xhr.setRequestHeader('Content-Type', 'application/json');
//     xhr.send(JSON.stringify({ postId: postId }));
// }

// // Function to handle the intersection observer callback
// function handleIntersection(entries) {
//     entries.forEach(entry => {
//         if (entry.isIntersecting) {
//             // The post is in the viewport
//             const postId = postElement.getAttribute('data-post-id'); // Get postId from data attribute
//             // Send an impression request when the post is in the viewport
//             sendImpression(postId);
//         }
//     });
// }

// // Create an Intersection Observer
// const observer = new IntersectionObserver(handleIntersection, {
//     root: null, // Use the viewport as the root
//     rootMargin: '0px',
//     threshold: 1.0, // Fire the callback when the post is fully in the viewport
// });

// // Add the posts to be observed
// document.addEventListener('DOMContentLoaded', function() {
//     const postElements = document.querySelectorAll('.user_post');
//     postElements.forEach(postElement => {
//         // Start observing each post element
//         console.log("Post seen")
//         observer.observe(postElement);
//     });
// });
