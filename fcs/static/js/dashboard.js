// accessing the DOM elements
const dels = document.querySelectorAll('#delete');

dels.forEach((del) => {
  del.addEventListener('click', function () {
    const modal = document.querySelector('.modal-2');
    story_id = del.dataset.storyid;
    modal.innerHTML = `<form action="delete_story/${story_id}" method="POST">
                <div class="text-right">
                  <a href="#" class="btn mr-5" role="button">Cancel</a>
                  <input
                    class="btn btn-primary"
                    type="submit"
                    value="Proceed"
                  />
                </div>
              </form>`;
  });
});
