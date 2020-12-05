// getting DOM Elements

const displaySwitch = document.getElementById("switch-2");
const body = document.querySelector("body");

// Setting Display Mode

setDisplay();

function setDisplay() {
  mode = localStorage.getItem("display-mode");
  if (mode) {
    if (mode == "dark") {
      displaySwitch.checked = "checked";
      body.className =
        "dark-mode with-custom-webkit-scrollbars with-custom-css-scrollbars";
    } else {
      displaySwitch.checked = "";
      body.className =
        "with-custom-webkit-scrollbars with-custom-css-scrollbars";
    }
  } else {
    localStorage.setItem("display-mode", "light");
    displaySwitch.checked = "";
    body.className = "with-custom-webkit-scrollbars with-custom-css-scrollbars";
  }
}

// changing display based on user definition

displaySwitch.addEventListener("click", () => {
  if (displaySwitch.checked) {
    localStorage.setItem("display-mode", "dark");
    setDisplay();
  } else {
    localStorage.setItem("display-mode", "light");
    setDisplay();
  }
});
// changing display based on user definition end
// Setting Display Mode end
