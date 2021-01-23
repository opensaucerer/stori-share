// getting elements from the DOM
const collections = document.querySelectorAll('#bcon');
const collections_box = document.querySelectorAll('.col-md-4');
// Getting elements from the DOM end

// lopping through each collections icon
collections.forEach((collection, index) => {
  const cid = collection.querySelector('#collections-id');

  collection.addEventListener('click', async function () {
    //calling API to update collections
    res = await fetch(`/collections/${cid.dataset.storyid}/remove`);
    data = await res.json();
    console.log(data, res.message);
    //removing collection from view
    if (data.message == 'success') {
      collections_box[index].style.display = 'none';
    }
  });
});
// lopping through each collections icon end
