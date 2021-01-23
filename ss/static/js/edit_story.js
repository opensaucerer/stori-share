//getting elements from the DOM
const form = document.querySelector('form');
const error1 = document.querySelector('#small1');
const error2 = document.querySelector('#small2');
const title = document.querySelector('#title');
const fb = document.querySelector('#fb');
const fg = document.querySelector('#fg');
const finput = document.querySelector('#file-input-6');
const fmsg = document.querySelector('.alert');
const msg = document.querySelector('.alert-heading');
const btn = document.querySelector('#submit');
const spin = document.querySelector('button i.fa');

const current_page = window.location.href;
const page_id = current_page.split('y/')[1].split('/')[0];
const story_id = parseInt(page_id);

title.addEventListener('input', function (event) {
  if (title.value.length == 0) {
    error1.innerText = "Title Can't be Empty";
  } else if (title.value.length > 0 && title.value.length <= 75) {
    error1.innerText = '';
  } else if (title.value.length > 75) {
    error1.innerText = 'Your Title is Too Long';
  }
});

// storied.addEventListener("input", function (event) {
//   var currentContent = tinymce.activeEditor.getContent();
//   if (currentContent.trim().length == 0 || currentContent.trim().length < 100) {
//     error2.innerText = "Your Story Is Too Short";
//   } else if (currentContent.trim().length >= 100) {
//     error2.innerText = "";
//   }
// });

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
  } else {
    event.preventDefault();
    error2.innerText = '';
    btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Updating';
    // spin.className = "fa fa-spinner fa-spin";
    // btn.innerText = "Publishing";
    if (finput.value) {
      const formData = new FormData();

      formData.append('story_image', finput.files[0]);

      response = await fetch(`/stories/story_upload`, {
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
            story_id: story_id,
          };
          const storyRes = await fetch(`/edit_story/<id>/edit`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(contentHTML),
          });
          if (storyRes.ok) {
            const storyData = await storyRes.json();
            console.log(storyData);
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
            console.log('failed to send');
            fmsg.className = 'alert alert-danger';
            fmsg.style.display = '';
            msg.innerText = "Your Story Wasn't Published. Please Try Again";
            spin.className = 'fa';
            btn.innerText = `Publish`;
          }
        } else {
          fmsg.className = 'alert alert-danger';
          fmsg.style.display = '';
          msg.innerText =
            'Image Upload Failed. Please Check File And Try Again';
          spin.className = 'fa';
          btn.innerText = `Publish`;
        }
      } else {
        console.log('failed to send');
        fmsg.className = 'alert alert-danger';
        fmsg.style.display = '';
        msg.innerText = 'Image Upload Failed. Please Check File And Try Again';
        spin.className = 'fa';
        btn.innerText = `Publish`;
      }
    } else {
      var contentHTML = {
        story_content: myContent,
        story_title: title.value,
        story_id: story_id,
        story_image: '',
      };
      const storyRes = await fetch(`/edit_story/<id>/edit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(contentHTML),
      });
      if (storyRes.ok) {
        const storyData = await storyRes.json();
        console.log(storyData);
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
        console.log('failed to send');
        fmsg.className = 'alert alert-danger';
        fmsg.style.display = '';
        msg.innerText = "Your Story Wasn't Published. Please Try Again";
        spin.className = 'fa';
        btn.innerText = `Publish`;
      }
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
