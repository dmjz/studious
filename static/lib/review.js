$( document ).ready(function() {

    // Get review data
    $.ajax({
        headers: { "X-CSRFToken": CSRF_TOKEN },
        url: AVAILABLE_REVIEWS_URL,
        method: 'GET',
        success: function(data) {
            console.log('success');
            console.log(data);
        },
        failure: function(data) {
            console.log('Now you fucked up'); 
        }
    });

});