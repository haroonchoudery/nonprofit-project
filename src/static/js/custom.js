$(function() {
    $('form#query').submit(function() 
    {
      $.getJSON('/score', {key: $('input[name="key"]').val()}, function(data){
        $("#score").text(data.revenue_growth);
      });
      return false;
    }
    );
  });
