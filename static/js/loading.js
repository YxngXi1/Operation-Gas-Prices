var text = 'Doing the math...';
var index = 0;
var isDeleting = false;
var a = 1;

function type() {
    var typing = document.getElementById('typing');
    typing.innerHTML = text.slice(0, index);
    if (isDeleting) {
        // If we're deleting, decrement the index
        index--;
    } else {
        // If we're typing, increment the index
        index++;
    }

    if (index > text.length) {
        // Start deleting after the entire text has been typed out
        isDeleting = true;
    } else if (index <= 0) {  // Changed condition here
        // Start typing again after the entire text has been deleted
        isDeleting = false;
    }

    // Repeat the function every 200 milliseconds if typing, 100 milliseconds if deleting
    var timeout = isDeleting ? 50 : 200;
    setTimeout(type, timeout);
}

// Start the typing animation
type();


document.addEventListener('DOMContentLoaded', function() {
    console.log('should start scraping');
    fetch('/scrape')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Ensure the response is processed as JSON
        })
        .then(data => {
            console.log(data); // Should log the object { message: "done scraping" }
            if (data.message === "done scraping") {
                // Navigate to /results if the scraping is done
                window.location.href = "/results";
            } else {
                console.error('Unexpected message:', data.message);
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});