const displaySwitch = document.getElementById("switch-2");
const body = document.querySelector("body");
// const submit = document.querySelector("#submit");
const form = document.querySelector("form");
const error1 = document.querySelector("#small1");
const error2 = document.querySelector("#small2");
const title = document.querySelector("#title");
const storied = document.querySelector(".editor");
const fb = document.querySelector("#fb");
const fg = document.querySelector("#fg");
const finput = document.querySelector("#file-input-6");
const fmsg = document.querySelector(".alert");
const msg = document.querySelector(".alert-heading");
const btn = document.querySelector("#submit");
const spin = document.querySelector("button i.fa");

console.log(spin);

var skin;
var theme;

title.addEventListener("input", function (event) {
  if (title.value.length == 0) {
    error1.innerText = "Title Can't be Empty";
  } else if (title.value.length > 0 && title.value.length <= 75) {
    error1.innerText = "";
  } else if (title.value.length > 75) {
    error1.innerText = "Your Title is Too Long";
  }
});

storied.addEventListener("input", function (event) {
  var currentContent = tinymce.activeEditor.getContent();
  if (currentContent.trim().length == 0 || currentContent.trim().length < 100) {
    error2.innerText = "Your Story Is Too Short";
  } else if (currentContent.trim().length >= 100) {
    error2.innerText = "";
  }
});

function setDisplay() {
  mode = localStorage.getItem("display-mode");
  if (mode) {
    if (mode == "dark") {
      displaySwitch.checked = "checked";
      body.className =
        "dark-mode with-custom-webkit-scrollbars with-custom-css-scrollbars";
      skin = "oxide-dark";
      theme = "dark";
    } else {
      displaySwitch.checked = "";
      body.className =
        "with-custom-webkit-scrollbars with-custom-css-scrollbars";
      skin = "oxide";
      theme = "default";
    }
  } else {
    localStorage.setItem("display-mode", "light");
    displaySwitch.checked = "";
    body.className = "with-custom-webkit-scrollbars with-custom-css-scrollbars";
  }
}
setDisplay();

displaySwitch.addEventListener("click", () => {
  if (displaySwitch.checked) {
    localStorage.setItem("display-mode", "dark");
    setDisplay();
    editor();
  } else {
    localStorage.setItem("display-mode", "light");
    setDisplay();
    editor();
  }
});

function editor() {
  tinymce.init({
    selector: ".editor",
    skin: skin,
    content_css: theme,
    inline: true,
    plugins: " autosave lists",
    autosave_interval: "10s",
    autosave_restore_when_empty: true,
    autosave_ask_before_unload: false,
    toolbar:
      "undo redo | styleselect | bold italic forecolor backcolor |" +
      "alignleft aligncenter alignright alignjustify |" +
      "bullist numlist outdent indent",
  });
}

editor();

btn.onclick = async function (event) {
  var myContent = tinymce.activeEditor.getContent();
  if (title.value.length == 0) {
    error1.innerText = "Title Can't be Empty";
    event.preventDefault();
  } else if (title.value.length > 78) {
    error1.innerText = "Your Title is Too Long";
    event.preventDefault();
  } else if (myContent.trim().length == 0 || myContent.trim().length < 100) {
    error2.innerText = "Your Story Is Too Short";
    event.preventDefault();
  } else if (!finput.value) {
    fg.classList.add("is-invalid");
    fb.innerText = "Story Image Required";
    event.preventDefault();
  } else {
    event.preventDefault();
    btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Publishing';
    // spin.className = "fa fa-spinner fa-spin";
    // btn.innerText = "Publishing";

    const formData = new FormData();

    formData.append("story_image", finput.files[0]);

    const response = await fetch(`/stories/story_upload`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data);
      if (data.status == "success") {
        var contentHTML = {
          story_content: myContent,
          story_title: title.value,
          story_image: data.path,
        };
        const storyRes = await fetch(`/stories/create_story`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(contentHTML),
        });
        if (storyRes.ok) {
          const storyData = await storyRes.json();
          console.log(storyData);
          if (storyData.status == "success") {
            window.location.href = storyData.link;
          } else {
            fmsg.className = "alert alert-danger";
            fmsg.style.display = "";
            msg.innerText = "Your Story Wasn't Published. Please Try Again";
            spin.className = "fa";
            btn.innerText = `Publish`;
          }
        } else {
          console.log("failed to send");
          fmsg.className = "alert alert-danger";
          fmsg.style.display = "";
          msg.innerText = "Your Story Wasn't Published. Please Try Again";
          spin.className = "fa";
          btn.innerText = `Publish`;
        }
      } else {
        fmsg.className = "alert alert-danger";
        fmsg.style.display = "";
        msg.innerText = "Image Upload Failed. Please Check File And Try Again";
        spin.className = "fa";
        btn.innerText = `Publish`;
      }
    } else {
      console.log("failed to send");
      fmsg.className = "alert alert-danger";
      fmsg.style.display = "";
      msg.innerText = "Image Upload Failed. Please Check File And Try Again";
      spin.className = "fa";
      btn.innerText = `Publish`;
    }
  }
};

var _validFileExtensions = [".jpg", ".jpeg", ".png"];
function ValidateSingleInput(oInput) {
  if (oInput.type == "file") {
    var sFileName = oInput.value;
    var sFileSize = oInput.files[0].size;
    if (sFileName.length > 0) {
      var blnValid = false;
      var bsize = false;
      for (var j = 0; j < _validFileExtensions.length; j++) {
        var sCurExtension = _validFileExtensions[j];
        if (sFileSize < 615000) {
          bsize = true;
          if (
            sFileName
              .substr(
                sFileName.length - sCurExtension.length,
                sCurExtension.length
              )
              .toLowerCase() == sCurExtension.toLowerCase()
          ) {
            blnValid = true;
            break;
          }
        }
      }

      if (!bsize) {
        fg.classList.add("is-invalid");
        fb.innerText = "File Too Large. No more than 600 KB";
        oInput.value = "";
        return false;
      } else if (!blnValid) {
        fg.classList.add("is-invalid");
        fb.innerText = "You can only upload image files with PNG, JPG, JPEG";
        oInput.value = "";
        return false;
      } else {
        fg.classList.remove("is-invalid");
        fb.innerText = "";
      }
    }
  }
  return true;
}
