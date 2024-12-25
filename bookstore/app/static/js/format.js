

$(document).ready(function(){

  $(window).scroll(function() {
    if ($(this).scrollTop() >= 50) {
      $("#header").css({
        "position" : "fixed",
        "top" : 0,
        "left" : 0,
        "right" : 0,
        "z-index" : 999,
      })
    } else{
      $("#header").css({
        "position": "static",
      })
    }
  });
});


