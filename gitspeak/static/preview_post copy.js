function goBack() {
    window.history.back();
  }

  // Default posts from backend
let linkedInPost = { linkedinPost }; // Correct escaping for JSON
let twitterPost = "{{ twitterPost | tojson | safe }}"; // Correct escaping for JSON

// Track any user edits to the posts
let editedLinkedInPost = linkedinPost;
let editedTwitterPost = twitterPost;
console.log("LinkedIn Post:", linkedInPost);
console.log("Twitter Post:", twitterPost);

document.addEventListener("DOMContentLoaded", function () {
    const postBody = document.getElementById("post-body");
    postBody.value = linkedInPost;  // Set LinkedIn post as default content
  });

  function switchPost(platform) {
    const linkedinButton = document.getElementById("linkedin-button");
    const xButton = document.getElementById("x-button");
    const postBody = document.getElementById("post-body");

    // Save the current content before switching
    if (linkedinButton.classList.contains("active")) {
        editedLinkedInPost = postBody.value; // Save edits for LinkedIn
    } else {
        editedTwitterPost = postBody.value; // Save edits for Twitter
    }
  
    // Switch to the selected platform's post
    if (platform === "linkedin") {
      linkedinButton.classList.add("active");
      xButton.classList.remove("active");
      postBody.value = editedLinkedInPost; // Load LinkedIn post (edited or default)
    } else {
      linkedinButton.classList.remove("active");
      xButton.classList.add("active");
      postBody.value = editedTwitterPost; // Load Twitter post (edited or default)
    }
  }
  
  function createPost() {
    // Get the current state of both posts
    const linkedinButton = document.getElementById("linkedin-button");
    const xButton = document.getElementById("x-button");
    const postBody = document.getElementById("post-body");
    
    // Save the latest edits before submission
    if (linkedinButton.classList.contains("active")) {
      editedLinkedInPost = postBody.value;
    } else if (xButton.classList.contains("active")) {
      editedTwitterPost = postBody.value;
    }

  
    // Send post content to the backend
    fetch("/normal_post/create_post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ editedLinkedInPost, editedTwitterPost }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Backend Response:", data);
      })
      .catch((error) => console.error("Error:", error));
  }
  