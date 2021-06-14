

// Increase cart count function
function increaseCartCount() {

    // Initialize new request
    const request = new XMLHttpRequest();
    request.open('POST', '{% url "increaseCartCount" %}');

    // Callback function for when request completes
    request.onload = () => {

        // Extract JSON data from request
        const data = JSON.parse(request.responseText);

        // Update display
        if (data.badge) {
            document.getElementById('badge').innerHTML = data.badge
            // console.log(`badge should now show ${data.badge}`)
        }
    }

    // Send request
    request.send();
}

// Decrease cart count function
function decreaseCartCount() {

    // Initialize new request
    const request = new XMLHttpRequest();
    request.open('POST', '{% url "decreaseCartCount" %}');

    // Callback function for when request completes
    request.onload = () => {

        // Extract JSON data from request
        const data = JSON.parse(request.responseText);

        // Update display
        if (data.badge) {
            document.getElementById('badge').innerHTML = data.badge
            // console.log(`badge should now show ${data.badge}`)
        }
    }

    // Send request
    request.send();
}

// Show messages in checkout
function showError(message) {
    document.getElementById('error-message').innerHTML = message
}