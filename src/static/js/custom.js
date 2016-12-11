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
                $('#error').hide();
                $('#results').hide();
            	var returnedData = JSON.parse(response);
                if(returnedData.name == null){
                    $('#error').show(1500);
                    console.log(response);
                    $('html, body').animate({
                        scrollTop: $("#notfound").offset().top
                    }, 2000);
                }
                else {
                    $('#name').text("Organization Name: " + returnedData.name);
                    $('#total_score').text("Score: " + returnedData.score);
                    $('#total_assets').text("Total Assets: $" + returnedData.total_assets);
                    $('#total_revenues').text("Total Revenues: $" + returnedData.total_revenues);
                    $('#net_assets').text("Net Assets: $" + returnedData.net_assets);
                    $('#results').show(1500);
                    console.log(response);
                    // scroll to results
                    $('html, body').animate({
                        scrollTop: $("#results").offset().top
                    }, 2000);
                }
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
