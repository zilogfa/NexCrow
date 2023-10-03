// toggle dark mode
function toggleDarkMode() {
    const html = document.querySelector("html"); // or document.body

    // Check if dark mode is enabled
    if (html.classList.contains("dark-mode")) {
        html.classList.remove("dark-mode");
        localStorage.setItem("dark-mode", "false");
    } else {
        html.classList.add("dark-mode");
        localStorage.setItem("dark-mode", "true");
    }
}

// Check if the user previously enabled dark mode
const isDarkMode = localStorage.getItem("dark-mode") === "true";

// Set the initial dark mode state based on the user's preference
if (isDarkMode) {
    document.querySelector("html").classList.add("dark-mode");
}

// Add a click event listener to the button
document.getElementById("dark-mode-toggle").addEventListener("click", toggleDarkMode);




// //  toggle dark mode

// function toggleDarkMode() {
//     const html = document.querySelector("html");

//     if (html.classList.contains("dark-mode")) {
//         html.classList.remove("dark-mode");
//         localStorage.setItem("dark-mode", "false");
//     } else {
//         html.classList.add("dark-mode");
//         localStorage.setItem("dark-mode", "true");
//     }
// }

// // Check if the user previously enabled dark mode
// const isDarkMode = localStorage.getItem("dark-mode") === "true";

// // Set the initial dark mode state based on the user's preference
// if (isDarkMode) {
//     toggleDarkMode(); // Apply dark mode immediately
// }

// // Add a click event listener to the button
// document.getElementById("dark-mode-toggle").addEventListener("click", toggleDarkMode);

