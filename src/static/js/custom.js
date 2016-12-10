// $(function() {
// 	var query = $('#query');

//     $(query).submit(function(){
//       $.getJSON('/score', {key: $('input[name="key"]').val()}, function(data){
//         // $("#score").text(data);
//         console.log(data);
//       });
//       return false;
//     });

//   });


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