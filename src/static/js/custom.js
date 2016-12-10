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
                console.log(returedData.revenue_growth);
                // $('#total_score').text(response.revenue_growth);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});