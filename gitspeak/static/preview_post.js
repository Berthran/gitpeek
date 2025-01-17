function goBack() {
    window.history.back();
  }

  let linkedInPost = "{{ linkedinPost }}"; // Default from backend
  let twitterPost = "{{ twitterPost | tojson | safe }}"; // Default from backend
  
// Track any user edits to the posts
let editedLinkedInPost = linkedInPost;
let editedTwitterPost = twitterPost;

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
    const linkedinPost = document.getElementById("linkedin-button").dataset.content || "";
    const twitterPost = document.getElementById("x-button").dataset.content || "";
  
    // Send post content to the backend
    fetch("/submit-post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ linkedinPost, twitterPost }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Backend Response:", data);
      })
      .catch((error) => console.error("Error:", error));
  }
  