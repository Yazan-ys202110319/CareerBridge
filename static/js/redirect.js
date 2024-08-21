function redirectToNextPage() {
    setTimeout(function() {
        window.location.href = "templates/home.html"
    }, 10000);
}

 // Redirect to the home page after a 3-second delay
 setTimeout(function() {
    window.location.href = "{{ url_for('home') }}";
}, 1000);