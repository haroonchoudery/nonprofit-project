$(function() {
	var query = $('#query');
	var key = $('#key');

    // $(query).bind('click', function(event) {
    //     $('html, body').animate({
    //          scrollTop: $("#results").offset().top
    //     }, 2000);
    //     return false;
    // });

    $(query).submit(function(event) {
        event.preventDefault();
        $.ajax({
            url: '/score',
            data: $(key).serialize(),
            type: 'POST',
            success: function(response) {
            	var returnedData = JSON.parse(response);
                $('#error').hide(1500);
                $('#results').hide(1500);
                if(returnedData.revenue_growth == null){
                    $('#error').show(1500);
                    console.log(response);
                    $('html, body').animate({
                        scrollTop: $("#results").offset().top
                    }, 2000);   
                }
                else {
                    $('#total_score').text("Score: " + returnedData.revenue_growth);
                    // var revenue_growth = returnedData.revenue_growth;
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