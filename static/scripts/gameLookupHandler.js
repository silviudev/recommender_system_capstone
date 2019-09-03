$(function() {
    $('#get_recs').click(function(){
      $.ajax({
          url: '/api/recs?id=' + document.getElementById("game_id").value,
          success: function(data) {
            console.log("AJAX WORKED!");
            console.log(data);
            $("#gameName").html(data["mainData"]["0"]["1"]);
            $("#gameImage").attr("src", data["mainData"]["0"]["13"]);
            $("#gameDescription").html(data["mainData"]["0"]["12"]);
          }
      });
    });
});
