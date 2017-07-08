$(document).ready(function(){
  $('.name').animate({left: 0}, 2000);

  $('.skills').animate({left: 0}, 2000);

  $('.scroll-button').click(function(){
    $('html, body').animate({
      scrollTop: $('.about').offset().top}, 1000);
    })
    
  $(".nav-about").click(function() {
    $('html,body').animate({
      scrollTop: $(".about").offset().top}, 'slow');
  });

  $(".nav-cartography").click(function() {
    $('html,body').animate({
      scrollTop: $(".cartography").offset().top - 50}, 'slow');
  });

  $(".nav-projects").click(function() {
    $('html,body').animate({
      scrollTop: $(".github").offset().top - 50}, 'slow');
  });
  });

$(window).scroll(function() {
    var aboutHeight = $(".about").outerHeight();
    if ($(this).scrollTop()>aboutHeight)
     {
      $('.navbar').fadeIn();
     }
    else
     {
      $('.navbar').fadeOut();
     }
 });
