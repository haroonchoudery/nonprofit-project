$(function() {
	var query = $('#query');
	var key = $('#key');

    $(query).submit(function(event) {
        // event.preventDefault();
        $(query).on('submit', function() {
            $('html, body').animate({
                 scrollTop: $("#results").offset().top
            }, 2000);
            return false;
        });
        $.ajax({
            url: '/score',
            data: $(key).serialize(),
            type: 'POST',
            success: function(response) {
            	var returnedData = JSON.parse(response);
                $('#total_score').text("Score: " + returnedData.revenue_growth);
                // var revenue_growth = returnedData.revenue_growth;
                $('#results').show(1500);
                console.log(response);	
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});