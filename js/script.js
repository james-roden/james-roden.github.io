$(document).ready(function(){
  $('.scroll-button').click(function(){
    $('html, body').animate({
      scrollTop: $('.page2').offset().top
    }, 1000);
    })
  })
