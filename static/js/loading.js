var text = 'Doing the math...';
var index = 0;
var isDeleting = false;
var a = 1;

function type() {
    var typing = document.getElementById('typing');
    console.log("display full word")
    typing.innerHTML = text.slice(0, index);
    if (isDeleting) {
        // If we're deleting, decrement the index
        console.log("decrease index");
        index--;
    } else {
        // If we're typing, increment the index
        console.log("increase index");
        index++;
    }

    if (index > text.length) {
        // Start deleting after the entire text has been typed out
        console.log('delete');
        isDeleting = true;
    } else if (index <= 0) {  // Changed condition here
        // Start typing again after the entire text has been deleted
        console.log('start typing');
        isDeleting = false;
    }

    // Repeat the function every 200 milliseconds if typing, 100 milliseconds if deleting
    var timeout = isDeleting ? 50 : 200;
    setTimeout(type, timeout);
    console.log('next letter');
}

// Start the typing animation
type();

// after 5 seconds animation stops
setTimeout(function() {
    window.location.href = "/results";
}, 6500);