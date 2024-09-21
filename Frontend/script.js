function displayImage(event) {
  const file = event.target.files[0];

  if (file) {
      EXIF.getData(file, function() {
          const lat = EXIF.getTag(this, "GPSLatitude");
          const latRef = EXIF.getTag(this, "GPSLatitudeRef");
          const lng = EXIF.getTag(this, "GPSLongitude");
          const lngRef = EXIF.getTag(this, "GPSLongitudeRef");

          const latitude = latRef === "N" ? convertToDecimal(lat) : -convertToDecimal(lat);
          const longitude = lngRef === "E" ? convertToDecimal(lng) : -convertToDecimal(lng);

          const itemId = document.getElementById("item-id").value; // Get item ID
          uploadFile(file, itemId, latitude, longitude);
      });
  }
}

function convertToDecimal(coord) {
  const degrees = coord[0];
  const minutes = coord[1] / 60;
  const seconds = coord[2] / 3600;
  return degrees + minutes + seconds; // Return as a float
}

function uploadFile(file, itemId, latitude, longitude) {
  const formData = new FormData();
  formData.append("item_id", parseInt(itemId)); // Convert item ID to integer
  formData.append("imagename", file.name); // Get the image name
  formData.append("latitude", latitude); // Append latitude
  formData.append("longitude", longitude); // Append longitude
  formData.append("file", file); // Append the actual file

  fetch("http://localhost:8080/upload_image/", {
      method: "POST",
      body: formData,
  })
  .then(response => response.json())
  .then(data => console.log("Success:", data))
  .catch(error => console.error("Error:", error));
}