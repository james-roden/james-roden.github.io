$(document).ready(function(){
  $('.name').animate({left: 0}, 2000);
  $('.skills').animate({left: 0}, 2000);
  $('.scroll-button').click(function(){
    $('html, body').animate({
      scrollTop: $('.about').offset().top}, 1000);
    })
  });

$(window).scroll(function() {
    var aboutHeight = $(".about").outerHeight()
    if ($(this).scrollTop()>aboutHeight)
     {
      $('.navbar').fadeIn();
     }
    else
     {
      $('.navbar').fadeOut();
     }
 });
