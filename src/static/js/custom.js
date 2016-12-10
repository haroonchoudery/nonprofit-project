$(function() {
    // Get the form.
    var form = $('#query');

    // Get the messages div.
    var formResults = $('#score');

    // TODO: The rest of the code will go here...
});

// Set up an event listener for the contact form.
$(function() {
    $('form').submit(function() {
        $.ajax({
            type: 'POST',
            url: '/score',
            data: formData;
        });
        return false;
    }); 
})

// Serialize the form data.
var formData = $(form).serialize();

// Submit the form using AJAX.

// 	.done(function(response) {
//     // Make sure that the formMessages div has the 'success' class.
//     $(formResults).removeClass('error');
//     $(formResults).addClass('success');

//     // Set the message text.
//     $(formResults).text(response);

//     // Clear the form.
//     $('#key').val('');
// })
// })

// .fail(function(data) {
//     // Make sure that the formMessages div has the 'error' class.
//     $(formMessages).removeClass('success');
//     $(formMessages).addClass('error');

//     // Set the message text.
//     if (data.responseText !== '') {
//         $(formMessages).text(data.responseText);
//     } else {
//         $(formMessages).text('Oops! An error occured and your message could not be sent.');
//     }
// });