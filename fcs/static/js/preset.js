// getting DOM Elements
const displaySwitch = document.getElementById('switch-2');
const body = document.querySelector('body');
const search = document.querySelector('#search');

// Setting Display Mode
setDisplay();

function setDisplay() {
  mode = localStorage.getItem('display-mode');
  if (mode) {
    if (mode == 'dark') {
      displaySwitch.checked = 'checked';
      body.className =
        'dark-mode with-custom-webkit-scrollbars with-custom-css-scrollbars';
    } else {
      displaySwitch.checked = '';
      body.className =
        'with-custom-webkit-scrollbars with-custom-css-scrollbars';
    }
  } else {
    localStorage.setItem('display-mode', 'light');
    displaySwitch.checked = '';
    body.className = 'with-custom-webkit-scrollbars with-custom-css-scrollbars';
  }
}

// changing display based on user definition

displaySwitch.addEventListener('click', () => {
  if (displaySwitch.checked) {
    localStorage.setItem('display-mode', 'dark');
    setDisplay();
  } else {
    localStorage.setItem('display-mode', 'light');
    setDisplay();
  }
});
// changing display based on user definition end
// Setting Display Mode end

//returning a message when the search icon is clicked
search.addEventListener('click', function (event) {
  event.preventDefault();
  halfmoon.initStickyAlert({
    content:
      "Thank's for using StoriShare. Our search functionality is coming soon",
    title: 'Search Is Coming Soon',
    alertType: 'alert-success',
    fillType: 'filled-lm',
  });
});
