$(function() {
    $('#get_recs').click(function(){
      $.ajax({
          url: '/api/recs?id=' + document.getElementById("game_id").value,
          success: function(data) {
            console.log("AJAX WORKED!");
            console.log(data);
            $("#topTenRecs").html(JSON.stringify(data,null," "));
          }
      });
    });
});
