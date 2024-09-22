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
  // Get the image name from the input field
  const imageName = document.getElementById("imageNameInput").value;

  // Validate that the image name is provided
  if (!imageName) {
      alert("Please enter an image name!");
      return;
  }

  // Build the request URL with the image name as a query parameter
  const url = `http://localhost:8000/result?imagename=${encodeURIComponent(imageName)}`;

  try {
      // Fetch the prediction from the FastAPI backend
      const response = await fetch(url);

      // Check if the response is OK (status code 200-299)
      if (!response.ok) {
          throw new Error("Network response was not OK");
      }

      // Parse the JSON data from the response
      const data = await response.json();

      // Check if there is an error in the response
      if (data.error) {
          alert("Error: " + data.error);
      } else {
          // Display the prediction value on the webpage
          const predictionDisplay = document.getElementById("predictionDisplay");
          predictionDisplay.textContent = `Prediction Value: ${data.value}%`;
      }
  } catch (error) {
      console.error("Error fetching prediction value:", error);
      alert("An error occurred while fetching the prediction.");
  }
}