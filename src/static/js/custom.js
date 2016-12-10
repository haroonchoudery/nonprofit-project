$(function() {
    $('#query').bind('click', function() {
      $.getJSON('/score', {
        key: $('input[name="key"]').val()
      }, function(data) {
        $("#score").text(data.score);
      });
      return false;
    });
  });
