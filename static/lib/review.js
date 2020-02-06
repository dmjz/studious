$( document ).ready(function() {

    console.log('sup bitch')

    // Get review data
    $.ajax({
        url: 'localhost:8000/review/available',
        success: function(data) {
            console.log('success');
            console.log(data);
        },
        failure: function(data) {
            console.log('Now you fucked up'); 
        }
    });

});