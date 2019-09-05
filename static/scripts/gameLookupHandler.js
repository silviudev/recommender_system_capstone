$(function() {
    $(document).ready(getRecs())

    function updatePage(data){
      console.log("AJAX WORKED!");
      console.log(data);
      $("#gameName").html(data["mainData"]["0"]["1"]);
      $("#gameImage").attr("src", data["mainData"]["0"]["13"]);
      $("#gameDescription").html(data["mainData"]["0"]["12"]);
      $("#gameID").html("ID: " + data["mainData"]["0"]["0"])
      $("#gameTags").html("Tags: " + data["mainData"]["0"]["7"].split(";").join(", "))
      $("#gameGenre").html("Genres: " + data["mainData"]["0"]["6"].split(";").join(", "))
      $("#gamePrice").html("Price: " + data["mainData"]["0"]["11"])
      $("#gameDate").html("Release Date: " + data["mainData"]["0"]["2"])
      $("#gameDeveloper").html("Developed by " + data["mainData"]["0"]["3"])
      $("#gamePublisher").html("Published By " + data["mainData"]["0"]["4"])
      $("#gamePositive").html("Postivie Ratings: " + data["mainData"]["0"]["8"])
      $("#gameNegative").html("Negative Ratings: " + data["mainData"]["0"]["9"])
      $("#gamePlatforms").html("Platform: " + data["mainData"]["0"]["5"].split(";").join(", "))

      for(let i = 0; i < data["recData"].length; i++){
        let queryString = "#rec" + (i+1)
        $(queryString + " figcaption").text("$" + data["recData"][i][2])
        $(queryString + " img").attr("src", data["recData"][i][3])
        $(queryString + " img").attr("alt", "Image for the recommended game " + data["recData"][i][1])
        $(queryString + " p").text(data["recData"][i][1])
        $("#rec_link" + (i+1)).attr("href", "?id=" + data["recData"][i][0])
      }
    }
    function getRecs(){
      $.ajax({
          url: '/api/recs' + window.location.search,
          success: updatePage
      });
    }
});
