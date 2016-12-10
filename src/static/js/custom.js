$(function() {
    $('form#query').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/score', {
        key: $('input[name="key"]').val()
      }, function(data) {
        $("#score").text(data.score);
      });
      return false;
    });
  });
