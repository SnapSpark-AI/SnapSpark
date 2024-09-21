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
  uploadBox.style.backgroundImage = "none";
  label.style.display = "block";
  closeIcon.style.display = "none";
  fileInput.value = "";
}

function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("item_id", 1);
  formData.append("imagename", file.name);
  formData.append("latitude", 0);
  formData.append("longitude", 0);

  fetch("http://127.0.0.1:8000/upload_image/", {
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
