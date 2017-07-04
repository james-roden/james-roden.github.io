var numberOfSquares = 6;
var colours = [];
var pickedColour;
var squares = document.querySelectorAll(".square");
var colourDisplay = document.getElementById("colourDisplay");
var messageDisplay = document.querySelector("#message");
var resetButton = document.querySelector("#reset");
var modeButtons = document.querySelectorAll('.mode');
var h1 = document.querySelector("h1");

init();

function init(){
  setupModeButtons();
  setupSquares();
  reset()
}

function setupModeButtons(){
  for (var i = 0; i < modeButtons.length; i++){
    modeButtons[i].addEventListener("click", function(){
      modeButtons[0].classList.remove("selected");
      modeButtons[1].classList.remove("selected");
      this.classList.add("selected");
      //figure out how many squares to show
      if (this.textContent === "Easy"){
        numberOfSquares = 3;
      } else{
        numberOfSquares = 6;
      }
      reset()
    });
  }
}

function setupSquares(){
  for (var i = 0; i < squares.length; i++){
    // add click events to squares
    squares[i].addEventListener("click", function(){
      //grab colour of clicked square
      var clickedColour = this.style.backgroundColor;
      //compare colour to picked colour
      if (clickedColour === pickedColour){
        messageDisplay.textContent = "Correct!";
        changeColours(clickedColour);
        h1.style.backgroundColor = clickedColour;
        resetButton.textContent = "Play Again?";
      } else{
        this.style.backgroundColor = "#232323";
        messageDisplay.textContent = "Try Again!";
      }
    })
  }
}

function reset(){
	colours = generateRandomColours(numberOfSquares);
	//pick a new random color from array
	pickedColour = pickColour();
	//change colorDisplay to match picked Color
	colourDisplay.textContent = pickedColour;
	resetButton.textContent = "New Colours"
	messageDisplay.textContent = "";
	//change colors of squares
	for(var i = 0; i < squares.length; i++){
		if(colours[i]){
			squares[i].style.display = "block"
			squares[i].style.background = colours[i];
		} else {
			squares[i].style.display = "none";
		}
	}
	h1.style.background = "steelblue";
}

resetButton.addEventListener("click", function(){
	reset();
})

function changeColours(colour){
  //loop through all squares and change colours
  for (var i = 0; i <squares.length; i++){
    squares[i].style.backgroundColor = colour;
  }
}

function pickColour(){
  var random = Math.floor(Math.random() * colours.length);
  return colours[random];
}

function generateRandomColours(n){
  //make an array
  arr = [];
  //add n random colours to array
  for (var i = 0; i < n; i++){
    //get random colour and push into array
    arr.push(randomColour());
  }
  //return that array
  return arr;
}

function randomColour(){
  //pick a "red" from 0-255
  var red = Math.floor(Math.random() * 256);
  //pick a "green" from 0-255
  var green = Math.floor(Math.random() * 256);
  //pick a "blue from 0-255"
  var blue = Math.floor(Math.random() * 256);
  return "rgb(" + red + ", " + green + (", ") + blue + ")";
}
