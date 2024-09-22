function displayImage(event) {
  const uploadBox = document.getElementById("upload-box");
  const file = event.target.files[0];
  const closeIcon = document.getElementById("close-icon");

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      uploadBox.style.backgroundImage = `url(${e.target.result})`;
      uploadBox.style.backgroundSize = "cover";
      uploadBox.style.backgroundPosition = "center";
      const label = uploadBox.querySelector(".upload-label");
      if (label) label.style.display = "none";
      closeIcon.style.display = "block";
      uploadFile(file);
    };
    reader.readAsDataURL(file);
  }
}

function resetImage() {
  const uploadBox = document.getElementById("upload-box");
  const fileInput = document.getElementById("file-upload");
  const closeIcon = document.getElementById("close-icon");
  const label = uploadBox.querySelector(".upload-label");

  // Reset the upload box to the initial state
  uploadBox.style.backgroundImage = "";
  label.style.display = "block";
  closeIcon.style.display = "none";
  fileInput.value = "";
}

function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  fetch("http://localhost:8000/upload_image", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("File uploaded successfully:", data);
    })
    .catch((error) => {
      console.error("Error uploading file:", error);
    });
}

function uploadAddress(address) {
  const formData = new FormData();
  formData.append("address", address);

  fetch("http://localhost:8000/put_address/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Address uploaded successfully:", data);
    })
    .catch((error) => {
      console.error("Error uploading address:", error);
    });
}

function displayResponse() {
  fetch("http://localhost:8000/ai-result")
    .then((response) => response.json())
    .then((data) => {
      const addressList = document.getElementById("addressList");
      addressList.innerHTML = "";

      data.forEach((address) => {
        const listItem = document.createElement("li");
        listItem.textContent = address;
        addressList.appendChild(listItem);
      });
    })
    .catch((error) => {
      console.error("Error fetching addresses:", error);
    });
}

function fetchPredictionValue() {
  fetch("http://localhost:8000/result")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Display the prediction value
      console.log("Prediction Value:", data.value);
      const predictionDisplay = document.getElementById("predictionDisplay");
      predictionDisplay.textContent = `Prediction: ${data.value}`;
    })
    .catch((error) => {
      console.error("Error fetching prediction value:", error);
    });
}

async function fetchPredictionRoboflow() {
  const imageName = document.getElementById("imageNameInput").value;

  if (!imageName) {
      alert("Please enter an image name!");
      return;
  }

  const url = `http://localhost:8000/result?imagename=${encodeURIComponent(imageName)}`;

  try {
      const response = await fetch(url);

      if (!response.ok) {
          throw new Error("Network response was not OK");
      }

      const data = await response.json();

      if (data.error) {
          alert("Error: " + data.error);
      } else {
          const predictionDisplay = document.getElementById("predictionDisplay");
          predictionDisplay.textContent = `Prediction Value: ${data.value}%`;
      }
  } catch (error) {
      console.error("Error fetching prediction value:", error);
      alert("An error occurred while fetching the prediction.");
  }
}

// Simulate sending a message and updating the chat interface
function sendMessage() {
  const message = document.getElementById('addressInput').value;
  if (message.trim() === "") return;

  // Create a new chat bubble for the user message
  const chatBox = document.getElementById('chatBox');
  const userMessage = document.createElement('div');
  userMessage.className = 'chat-message user';
  userMessage.innerText = message;
  chatBox.appendChild(userMessage);

  // Clear the input field
  document.getElementById('addressInput').value = "";

  // Simulate SparkChat response
  setTimeout(() => {
    const botMessage = document.createElement('div');
    botMessage.className = 'chat-message sparkchat';
    botMessage.innerText = "SparkChat: Thanks for your message!";
    chatBox.appendChild(botMessage);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom of the chat
  }, 1000);
}

function fetchPredictionValue() {
  // This function will handle fetching and displaying the prediction
  const chatBox = document.getElementById('chatBox');
  const botMessage = document.createElement('div');
  botMessage.className = 'chat-message sparkchat';
  botMessage.innerText = "Fetching prediction data...";
  chatBox.appendChild(botMessage);
  chatBox.scrollTop = chatBox.scrollHeight;
}