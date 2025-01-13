document.addEventListener('DOMContentLoaded', function() {
    const scaffold = document.getElementById('scaffold');
    
    // Mimicking the GestureDetector behavior
    scaffold.addEventListener('click', function(event) {
      if (!event.target.closest('.container')) {
        document.activeElement.blur();
      }
    });
  
    // Handling button clicks (example for the "Normal Post" button)
    const normalPostButton = document.querySelector('.normal-post-button');
    normalPostButton.addEventListener('click', function() {
      // Add functionality for "Normal Post" button here (e.g., navigating to a new page)
      console.log('Normal Post button clicked');
    });
  
    // Handling button clicks (example for the "Challenge Post" button)
    const challengePostButton = document.querySelector('.challenge-post-button');
    challengePostButton.addEventListener('click', function() {
      // Add functionality for "Challenge Post" button here (e.g., a simple log or action)
      console.log('Challenge Post button clicked');
    });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    const allPostsButton = document.querySelector('.all-posts');
    const normalPostButton = document.querySelector('.normal-post');
  
    // Function to handle "All" button click
    allPostsButton.addEventListener('click', function() {
      console.log('All button clicked');
      // Additional functionality can be added here (e.g., display all posts)
    });
  
    // Function to handle "Normal" button click
    normalPostButton.addEventListener('click', function() {
      console.log('Normal button clicked');
      // Additional functionality can be added here (e.g., display normal posts)
    });
  });

  document.addEventListener('DOMContentLoaded', function() {
    const challengeButton = document.querySelector('.challenge-button');
  
    // Function to handle "Challenge" button click
    challengeButton.addEventListener('click', function() {
      console.log('Challenge button clicked');
      // Additional functionality can be added here (e.g., show challenge details)
    });
  });
  
  