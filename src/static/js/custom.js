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
            	var returnedData = JSON.parse(response);
                $('#total_score').text(returnedData.revenue_growth);
                console.log(response);	
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});