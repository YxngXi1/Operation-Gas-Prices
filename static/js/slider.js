var slider = document.getElementById("myRange");
var inputField = document.getElementById("inputField");

inputField.value = slider.value;

slider.oninput = function() {
  inputField.value = this.value;
}

inputField.oninput = function() {
  slider.value = this.value;
}

inputField.onblur = function() {
  if (this.value > 1000) {
    this.value = 1000;
  } else if (this.value < 0) {
    this.value = 0;
  }
  slider.value = this.value;
}