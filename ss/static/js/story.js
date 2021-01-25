//data-sidebar-hidden
// getting DOM Elements

// Setting sidebar Mode
// getting elements from the DOM
const clikes = document.querySelectorAll('#lcon');
console.log(clikes);
// Getting elements from the DOM end

// lopping through each thumps_up icon
clikes.forEach((like) => {
  //getting story-id element
  const lid = like.querySelector('#story-id');
  // adding click event to each thumb_up icon
  lid.addEventListener('click', function () {
    if (lid.classList == 'fa fa-heart clicked') {
      // calling API to update number of likes
      async function addLikes() {
        res = await fetch(`/comments/like/${lid.dataset.storyid}/unlike`);
        data = await res.json();
        console.log(data, res.status);

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
        console.log(data, res.status);

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
