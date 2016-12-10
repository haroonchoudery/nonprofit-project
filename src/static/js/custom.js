$(function() {
	var query = $('#query');
	var key = $('#key');

    $(query).submit(function(event) {
    	event.preventDefault();
        $.ajax({
            url: '/score',
            data: $(key).serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                return revenue_growth;
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});