// We are adding a listener to the ul, this is always part of the page.
//When a selector is provided, the event handler is referred to as
//delegated. The handler is not called when the event occurs directly on the bound
//element, but only for descendants (inner elements) that match the selector. jQuery
//bubbles the event from the event target up to the element where the handler is attached
//(i.e., innermost to outermost element) and runs the handler for any elements
//along that path matching the selector.
//The li inside on is basically saying "when an li INSIDE of ul is clicked, do folloiwng"...

// Check off specific todos by clicking
$("ul").on("click", "li", function(){
  // Toggle list item
  $(this).toggleClass("completed");
});

// Click on delete to remove todo
$("ul").on("click", "span", function(event){
  // Fade out and remove parent of span, ie. li
  $(this).parent().fadeOut(500, function(){
    $(this).remove();
  });
  // Stop event bubbling
  event.stopPropagation();
})

// Add to todo when enter is clicked. enter code is 13
$("input[type='text']").keypress(function(event){
  if (event.which === 13){
    // Grab text from input
    var todoText = $(this).val();
    $(this).val("");
    // Create new li and add to ul
    $("ul").append("<li><span><i class='fa fa-trash'></i></span> " + todoText + "</li>")
  }
})

// Toggle input box when plus is clicked
$(".fa-plus").click(function(){
  $("input[type='text']").fadeToggle();
})
