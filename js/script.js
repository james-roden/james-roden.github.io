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
      //$('.navbar').fadeOut();
    }
  });

  $(".nav-about").click(function() {
    $('html, body').animate({
      scrollTop: $("#aboutme").offset().top - 100}, 1000);
  });

  $(".nav-code").click(function() {
    $('html, body').animate({
      scrollTop: $("#code").offset().top - 100}, 1000);
      TweenMax.staggerFrom("#code .content-card", 0.5, {x:-1000, scale:0.5, opacity:0, delay:0.2}, 0.2);
  });

  $(".nav-arcgis").click(function() {
    $('html, body').animate({
      scrollTop: $("#arcgis").offset().top - 100}, 1000);
      TweenMax.staggerFrom("#arcgis .content-card", 0.5, {x:-1000, scale:0.5, opacity:0, delay:0.2}, 0.2);
  });

  $(".nav-webgis").click(function() {
    $('html, body').animate({
      scrollTop: $("#aboutme").offset().top - 100}, 1000);
  });

  $(".nav-cartography").click(function() {
    $('html, body').animate({
      scrollTop: $("#cartography").offset().top - 100}, 1000);
      // TweenMax.from("#cartography .content-card", 0.5, {y:-1000, opacity:0, delay:0.2});
  });

});
