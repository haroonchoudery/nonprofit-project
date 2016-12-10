$(function() {
    $('#query').submit(function() {
      $.getJSON('/score', {key: $('input[name="key"]').val()}, function(data){
        console.log(data);
      });
      return false;
    });
  });
