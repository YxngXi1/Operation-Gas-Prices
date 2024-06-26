document.addEventListener('DOMContentLoaded', function() {
    // Toggle dropdown visibility
    document.getElementById("dropdownButton").addEventListener('click', function() {
        var content = document.querySelector(".dropdown-content");
        content.classList.toggle("show-dropdown"); // Use class to control visibility
    });

    // Close the dropdown when clicking outside of it
    window.addEventListener('click', function(event) {
        if (!event.target.matches('#dropdownButton')) {
            var dropdowns = document.querySelectorAll(".dropdown-content");
            dropdowns.forEach(function(dropdown) {
                if (dropdown.classList.contains("show-dropdown")) {
                    dropdown.classList.remove("show-dropdown");
                }
            });
        }
    });
});