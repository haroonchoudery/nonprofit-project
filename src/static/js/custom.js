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
                // $('#total_score').text(returnedData.revenue_growth);
                var revenue_growth = returnedData.revenue_growth;
                $('#results').show();
                console.log(response);	
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});