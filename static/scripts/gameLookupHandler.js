$(function() {
    function updatePage(data){
      console.log("AJAX WORKED!");
      console.log(data);
      $("#gameName").html(data["mainData"]["0"]["1"]);
      $("#gameImage").attr("src", data["mainData"]["0"]["13"]);
      $("#gameDescription").html(data["mainData"]["0"]["12"]);

      for(let i = 0; i < data["recData"].length; i++){
        let queryString = "#rec" + (i+1)
        $(queryString + " p").text(data["recData"][i][1])
        $(queryString + " figcaption").text(data["recData"][i][2])
        $(queryString + " img").attr("src", data["recData"][i][3])
        $(queryString + " img").attr("alt", "Image for the recommended game " + data["recData"][i][1])
        $("#rec_link" + (i+1)).attr("href", "/api/recs?id=" + data["recData"][i][0])
      }
    }
    function getRecs(){
      $.ajax({
          url: '/api/recs?id=' + document.getElementById("game_id").value,
          success: updatePage
      });
    }
    function getRecsFromLink(e){
      console.log(this)
      e.preventDefault()
      $.get({
          url: this.href,
          success: updatePage
      });
    }
    $('#get_recs').click(getRecs);
    $(".recs_link").click(getRecsFromLink);
});
