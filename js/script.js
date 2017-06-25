$(document).ready(function(){
  $('.name').animate({left: 0}, 2000);
  $('.skills').animate({left: 0}, 2000);
  $('.scroll-button').click(function(){
    $('html, body').animate({
      scrollTop: $('.page2').offset().top}, 1000);
    })
  });



$(window).scroll(function() {
    var aboutHeight = $(".page2").outerHeight()
    if ($(this).scrollTop()>aboutHeight)
     {
      $('.navbar').fadeIn();
     }
    else
     {
      $('.navbar').fadeOut();
     }
 });
