$(function() {
    $('#query').submit(function() 
    {
      $.getJSON('/score', {key: $('input[name="key"]').val()}, function(data){
        $("#score").text(data);
      });
      return false;
    }
    );
  });
