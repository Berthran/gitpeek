document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.form-content');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        // Remove active class from all tabs
        tabs.forEach(t => t.classList.remove('active'));
        // Hide all content
        contents.forEach(c => c.classList.add('hidden'));

        // Activate the clicked tab and its content
        tab.classList.add('active');
        const target = document.getElementById(tab.getAttribute('data-tab'));
        target.classList.remove('hidden');
      });
    });
  });