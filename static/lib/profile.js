$( document ).ready(function() {

    // Enable/disable delete button based on value of text input
    $('#delete-confirm-input').on('keyup', function(e) {
        var input  = $('#delete-confirm-input'),
            button = $('#delete-final-button');
        if (input.val() == 'DELETE') { 
            button.removeClass('disabled');
            button.removeAttr("disabled");
        }
        else { 
            button.addClass('disabled'); 
            button.attr('disabled', true);
        }
    });

});