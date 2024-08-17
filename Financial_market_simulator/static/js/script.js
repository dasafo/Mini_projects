document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('userModal');
    const openModalBtn = document.getElementById('openModalBtn');
    const closeBtn = document.getElementsByClassName('closeBtn')[0];

    // Open the modal
    openModalBtn.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    // Close the modal when the close button is clicked
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Close the modal when clicking outside of the modal content
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Optionally, you can close the modal after the form is submitted
    const form = document.getElementById('createUserForm');
    form.addEventListener('submit', function() {
        modal.style.display = 'none';
    });
});
