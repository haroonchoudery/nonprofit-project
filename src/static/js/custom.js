$(function() {
	var query = $('#query');
	var key = $('input[name="key"]').val();
    $(query).submit(function() {
        $.ajax({
            url: '/score',
            data: $(key).serialize(),
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