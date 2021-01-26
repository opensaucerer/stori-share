// getting elements from the DOM
const flikes = document.querySelectorAll('#lcon');
const fcontent = document.querySelector('textarea');
const fbtn = document.querySelector('#feedback');
// Getting elements from the DOM end

//enabling users to like feedbacks
// lopping through each thumps_up icon
flikes.forEach((like) => {
  //getting story-id element
  const lid = like.querySelector('#story-id');
  // adding click event to each thumb_up icon
  lid.addEventListener('click', function () {
    if (lid.classList == 'fa fa-heart clicked') {
      // calling API to update number of likes
      async function addLikes() {
        res = await fetch(`/comments/like/${lid.dataset.storyid}/unlike`);
        data = await res.json();
        // console.log(data, res.status);

        if (data.status == 'success') {
          like.querySelector('.lspan').innerText = data.count;
          lid.classList.toggle('clicked');
        }
      }
      addLikes();
    } else {
      // calling API to update number of likes

      async function addLikes() {
        res = await fetch(`/comments/like/${lid.dataset.storyid}/like`);

        data = await res.json();
        // console.log(data, res.status);

        if (data.status == 'success') {
          like.querySelector('.lspan').innerText = data.count;
          lid.classList.toggle('clicked');
        }
      }
      addLikes();
    }
  });
});
// adding click event to each thumb_up icon end
// lopping through each thumps_up icon end
//enabling users to like feedback end

//enabling users to add new feedback
fbtn.onclick = async function () {
  if (fcontent.value.length == 0) {
    document.querySelector('#error').innerText = "Your feedback can't be empty";
    return;
  }

  if (fcontent.value.split(' ').length < 3) {
    document.querySelector('#error').innerText = 'Your feedback is too short';
    return;
  }

  comment = {
    content: fcontent.value,
    story_id: likes[0].querySelector('#story-id').dataset.storyid,
  };

  document.querySelector('#error').innerText = '';

  const response = await fetch(`/comments/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(comment),
  });

  if (response.ok) {
    const data = await response.json();

    //checking request status
    if (data.message == 'success') {
      //updating feedbacks on success
      fcon = document.querySelector('.feedback_container');
      nfcon = document.querySelector('.no_feedback_container');
      nfmsg = document.querySelector('.no_feedback_message');

      comment = `<div class="feedback">
          <a
          href="${data.data.author}"
          class="nav-link user"
          style="width: fit-content"
            >
            <img
                src="${window.location.origin}/static/img/profile_pic/${data.data.img}"
                class="img-fluid"
                alt="Profile Picture"
                style="border: 1px solid grey; border-radius: 50%"
              />
              <small
              style="
                  color: #1890ff;
                  font-weight: 700;
                  font-size: 1.3rem;
                  letter-spacing: 1px;
                "
                class="pl-5"
                >${data.data.author}</small
                >
                </a>
                
                <p class="sidebar-link">${data.data.content}</p>
            <div class="sidebar-link">
            <div class="d-flex justify-content-between align-items-center">
                <div >
                  </div>
                  
                  <div class="btn-group">
                  a few seconds ago
                </div>
                </div>
            </div>
            <div class="sidebar-divider"></div>
            </div>`;

      if (fcon) {
        fcon.innerHTML = comment + fcon.innerHTML;
        fcontent.value = '';
      } else {
        nfmsg.innerHTML = '';
        nfcon.innerHTML = comment + nfcon.innerHTML;
        fcontent.value = '';
      }
      new_flikes = document.querySelectorAll('#lcon');

      new_flikes.forEach((like) => {
        //getting story-id element
        const lid = like.querySelector('#story-id');
        // adding click event to each thumb_up icon
        lid.addEventListener('click', function () {
          if (lid.classList == 'fa fa-heart clicked') {
            // calling API to update number of likes
            async function addLikes() {
              res = await fetch(`/comments/like/${lid.dataset.storyid}/unlike`);
              dat = await res.json();
              // console.log(data, res.status);

              if (dat.status == 'success') {
                like.querySelector('.lspan').innerText = dat.count;
                lid.classList.toggle('clicked');
              }
            }
            addLikes();
          } else {
            // calling API to update number of likes

            async function addLikes() {
              res = await fetch(`/comments/like/${lid.dataset.storyid}/like`);

              dat = await res.json();
              // console.log(data, res.status);

              if (dat.status == 'success') {
                like.querySelector('.lspan').innerText = dat.count;
                lid.classList.toggle('clicked');
              }
            }
            addLikes();
          }
        });
      });
    }
  } else {
    // alerting the user on fail
    halfmoon.initStickyAlert({
      content: 'Failed to send feedback',
      alertType: 'alert-danger',
      fillType: 'filled-lm',
    });
  }
};
//enabling users to add new feedback end
