$(document).ready(function(){
  $('.name').animate({left: 0}, 2000);

  $('.skills').animate({left: 0}, 2000);

  $('.social').animate({left: 0}, 2000);

  $(".nav-about").click(function() {
    $('html, body').animate({
      scrollTop: $("#aboutme").offset().top - 100}, 1000);
  });

  $(".nav-work").click(function() {
    $('html, body').animate({
      scrollTop: $("#code").offset().top - 100}, 1000);
  });

  $(".nav-arcgis").click(function() {
    $('html, body').animate({
      scrollTop: $("#arcgis").offset().top - 100}, 1000);
  });

});
