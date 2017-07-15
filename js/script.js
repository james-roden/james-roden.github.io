$(document).ready(function(){
  $('.name').animate({left: 0}, 2000);

  $('.skills').animate({left: 0}, 2000);

  $('.scroll-button').click(function(){
    $('body').animate({
      scrollTop: $('#aboutme').offset().top - 100}, 1000);
    })

  window.addEventListener("scroll", function() {
    var windowHeight = $(window).height() - 50;
    if (window.scrollY > windowHeight) {
      $('.navbar').fadeIn();
    }
    else {
      $('.navbar').fadeOut();
    }
  });

  $(".nav-about").click(function() {
    $('html, body').animate({
      scrollTop: $("#aboutme").offset().top - 100}, 1000);
  });

  $(".nav-code").click(function() {
    $('html, body').animate({
      scrollTop: $("#code").offset().top - 100}, 1000);
  });

  $(".nav-arcgis").click(function() {
    $('html, body').animate({
      scrollTop: $("#arcgis").offset().top - 100}, 1000);
  });

  $(".nav-webgis").click(function() {
    $('html, body').animate({
      scrollTop: $("#aboutme").offset().top - 100}, 1000);
  });

  $(".nav-cartography").click(function() {
    $('html, body').animate({
      scrollTop: $("#cartography").offset().top - 100}, 1000);
  });
});
