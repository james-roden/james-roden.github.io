$(document).ready(function(){
  $('.page1').hide();
  $('.page1').fadeIn(1000);
  $('.scroll-button').click(function(){
    $('html, body').animate({
      scrollTop: $('.page2').offset().top
    }, 1000);
  })})
