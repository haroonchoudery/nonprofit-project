$(function() {
	var query = $('#query');

    $(query).submit(function(event) {
    	event.preventDefault();
        $.ajax({
            url: '/score',
            data: $('input[name="key"]').val().serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});