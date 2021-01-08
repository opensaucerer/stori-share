//getting elements from the DOM
const form = document.querySelector('form');
const error1 = document.querySelector('#small1');
const error2 = document.querySelector('#small2');
const title = document.querySelector('#title');
// const storied = document.querySelector(".note-editable");
const fb = document.querySelector('#fb');
const fg = document.querySelector('#fg');
const finput = document.querySelector('#file-input-6');
const fmsg = document.querySelector('.alert');
const msg = document.querySelector('.alert-heading');
const btn = document.querySelector('#submit');
const spin = document.querySelector('button i.fa');

//instantiating the summernoteJS html editor
$(document).ready(function () {
  $('#editor').summernote({
    placeholder: 'Remember, Any Story Can Be Told',
    tabsize: 1,
    height: 200,
    toolbar: [
      // [groupName, [list of button]]
      ['style', ['bold', 'italic', 'underline', 'clear']],
      ['font', ['strikethrough', 'superscript', 'subscript']],
      ['para', ['ul', 'ol', 'paragraph']],
      ['insert', ['link']],
    ],
    dialogsFade: true,
  });
});

title.addEventListener('input', function (event) {
  if (title.value.length == 0) {
    error1.innerText = "Title Can't be Empty";
  } else if (title.value.length > 0 && title.value.length <= 75) {
    error1.innerText = '';
  } else if (title.value.length > 75) {
    error1.innerText = 'Your Title is Too Long';
  }
});

btn.onclick = async function (event) {
  var myContent = $('#editor').summernote('code');
  if (title.value.length == 0) {
    error1.innerText = "Title Can't be Empty";
    event.preventDefault();
  } else if (title.value.length > 78) {
    error1.innerText = 'Your Title is Too Long';
    event.preventDefault();
  } else if (myContent.trim().length == 0 || myContent.trim().length < 100) {
    error2.innerText = 'Your Story Is Too Short';
    event.preventDefault();
  } else if (!finput.value) {
    fg.classList.add('is-invalid');
    fb.innerText = 'Story Image Required';
    error2.innerText = '';
    event.preventDefault();
  } else {
    event.preventDefault();
    btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Publishing';

    const formData = new FormData();

    formData.append('story_image', finput.files[0]);

    const response = await fetch(`/stories/story_upload`, {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      // console.log(data);
      if (data.status == 'success') {
        var contentHTML = {
          story_content: myContent,
          story_title: title.value,
          story_image: data.path,
        };
        const storyRes = await fetch(`/stories/create_story`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(contentHTML),
        });
        if (storyRes.ok) {
          const storyData = await storyRes.json();
          // console.log(storyData);
          if (storyData.status == 'success') {
            window.location.href = storyData.link;
          } else {
            fmsg.className = 'alert alert-danger';
            fmsg.style.display = '';
            msg.innerText = "Your Story Wasn't Published. Please Try Again";
            spin.className = 'fa';
            btn.innerText = `Publish`;
          }
        } else {
          // console.log("failed to send");
          fmsg.className = 'alert alert-danger';
          fmsg.style.display = '';
          msg.innerText = "Your Story Wasn't Published. Please Try Again";
          spin.className = 'fa';
          btn.innerText = `Publish`;
        }
      } else {
        fmsg.className = 'alert alert-danger';
        fmsg.style.display = '';
        msg.innerText = 'Image Upload Failed. Please Check File And Try Again';
        spin.className = 'fa';
        btn.innerText = `Publish`;
      }
    } else {
      // console.log("failed to send");
      fmsg.className = 'alert alert-danger';
      fmsg.style.display = '';
      msg.innerText = 'Image Upload Failed. Please Check File And Try Again';
      spin.className = 'fa';
      btn.innerText = `Publish`;
    }
  }
};

var _validFileExtensions = ['.jpg', '.jpeg', '.png'];
function ValidateSingleInput(oInput) {
  if (oInput.type == 'file') {
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
        fg.classList.add('is-invalid');
        fb.innerText = 'File Too Large. No more than 600 KB';
        oInput.value = '';
        return false;
      } else if (!blnValid) {
        fg.classList.add('is-invalid');
        fb.innerText = 'You can only upload image files with PNG, JPG, JPEG';
        oInput.value = '';
        return false;
      } else {
        fg.classList.remove('is-invalid');
        fb.innerText = '';
      }
    }
  }
  return true;
}
