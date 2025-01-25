function goBack() {
    window.history.back();
  }

  // Default posts from backend
let linkedInPost = { linkedinPost | tojson  | safe }; // Correct escaping for JSON
let twitterPost = "{{ twitterPost | tojson | safe }}"; // Correct escaping for JSON

// Track any user edits to the posts
let editedLinkedInPost = linkedInPost;
let editedTwitterPost = twitterPost;

console.log("LinkedIn Post:", linkedInPost);
console.log("Twitter Post:", twitterPost);

document.addEventListener("DOMContentLoaded", function () {
    const postBody = document.getElementById("post-body");
    postBody.value = linkedInPost;  // Set LinkedIn post as default content
  });

  function switchPost(platform) {
    const postBody = document.getElementById('post-body');
    const buttons = document.querySelectorAll('.toggle-button');
  
    buttons.forEach(button => {
      button.classList.remove('active');
    });
  
    document.getElementById(`${platform}-button`).classList.add('active');
  
    const selectedPost = document.getElementById(`${platform}-button`).getAttribute('data-content');
    postBody.value = selectedPost;
  }
  
  function createPost() {
    const postBody = document.getElementById('post-body').value;
    const activeButton = document.querySelector('.toggle-button.active');
    const platform = activeButton.id.replace('-button', ''); // Get platform (linkedin or x)
  
    // Prepare data based on the platform
    let postData;
    if (platform === 'linkedin') {
      // Prepare LinkedIn post data (replace with your actual data structure)
      postData = {
        // ... your LinkedIn post data ...
      };
    } else if (platform === 'x') {
      // Prepare X (Twitter) post data (replace with your actual data structure)
      postData = {
        // ... your X (Twitter) post data ...
      };
    }
  
    // Escape JSON for both platforms
    const escapedPostData = JSON.stringify(postData);
  
    // Make API call to create the post
    fetch(`/api/${platform}/create`, { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: escapedPostData
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Post created successfully:', data);
      // Handle success (e.g., display a success message to the user)
    })
    .catch(error => {
      console.error('Error creating post:', error);
      // Handle error (e.g., display an error message to the user)
    });
  }