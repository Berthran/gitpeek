document.addEventListener("DOMContentLoaded", () => {
    const copyButtons = document.querySelectorAll(".copy-icon");
  
    // Add copy functionality to each button
    copyButtons.forEach(button => {
      button.addEventListener("click", () => {
        const targetId = button.getAttribute("data-target");
        const textField = document.getElementById(targetId);
  
        if (textField) {
          // Copy the content to the clipboard
          navigator.clipboard.writeText(textField.value)
            .then(() => {
              alert(`Copied successfully!`);
            })
            .catch(err => {
              console.error("Failed to copy text: ", err);
            });
        }
      });
    });
  });
  