$(function() {
    // create variable for form div and search input
	var query = $('#query');
	var key = $('#key');


    $(query).submit(function(event) {
        // prevent form from redirecting to different URL
        event.preventDefault();
        $.ajax({
            // serialize data and send to Flask controller
            url: '/score',
            data: $(key).serialize(),
            type: 'POST',

            success: function(response) {
                $('#error').hide();
                $('#results').hide();
            	var returnedData = JSON.parse(response);

                // if null is returned, display notfound.html and scroll down to result
                if(returnedData.name == null){
                    $('#error').show(1500);
                    console.log(response);
                    $('html, body').animate({
                        scrollTop: $("#notfound").offset().top
                    }, 2000);
                }

                // otherwise, return all below data and scroll down to displayed data
                else {
                    $('#name').text("Name: " + returnedData.name);
                    $('#total_score').text("Score: " + returnedData.score);
                    $('#type').text("Tax Status: " + returnedData.tax_status);
                    $('#tax_year').text("Tax Year: " + returnedData.tax_year);
                    $('#score_percentile').text("Score Percentile: " + returnedData.score_percentile);
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



// scroll animation for anchor tags
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});
