var frontCamera = false;
var currentStream;

// Define constants
// Get the element in the document with id="camera-view", "camera-device", "photo-display", "take-photo-button" and "front-camera-button"
const cameraView = document.querySelector("#camera-view"),
  cameraDevice = document.querySelector("#camera-device"),
  photoDisplay = document.querySelector("#photo-display"),
  takePhotoButton = document.querySelector("#take-photo-button"),
  sendPhotoButton = document.querySelector("#send-photo-button"),
  frontCameraButton = document.querySelector("#front-camera-button");

// Access the device camera and stream to cameraDevice
function cameraStart() {
  // Stop the video streaming before access the media device
  if (typeof currentStream !== "undefined") {
    currentStream.getTracks().forEach((track) => {
      track.stop();
    });
  }

  // Set constraints for the video stream
  // If frontCamera is true, use front camera
  // Otherwise, user back camera
  // "user" => Front camera
  // "environment" => Back camera
  var constraints = {
    video: { facingMode: frontCamera ? "user" : "environment" },
    audio: false,
  };

  // Access the media device, camera in this example
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      currentStream = stream;
      cameraDevice.srcObject = stream;
    })
    .catch(function (error) {
      console.error("Error happened.", error);
    });
}


// If takePhotoButton clicked => Take and display a photo
takePhotoButton.onclick = function () {
  cameraView.width = cameraDevice.videoWidth;
  cameraView.height = cameraDevice.videoHeight;
  cameraView.getContext("2d").drawImage(cameraDevice, 0, 0);
  photoDisplay.src = cameraView.toDataURL("image/webp");
  photoDisplay.classList.add("photo-taken");
};

// If Front/Back camera is click => Change to front/back camera accordingly
frontCameraButton.onclick = function () {
  // Toggle the frontCamera variable
  frontCamera = !frontCamera;
  // Setup the button text
  if (frontCamera) {
    frontCameraButton.textContent = "후면 카메라";
  } else {
    frontCameraButton.textContent = "전면 카메라";
  }
  // Start the video streaming
  cameraStart();
};

// 
// sendbutton누르면 image url(photoDisplay.src) 형식 바꿔서 보내줌 
sendPhotoButton.onclick = () => {
  if (photoDisplay.src) {
    sendDataUrlViaForm(photoDisplay.src);
  } 
  else {
    alert("사진을 먼저 찍어주세요!");
  }
}
// Data URL을 Blob 객체로 변환하는 함수
function dataURLToBlob(dataUrl) {
  var arr = dataUrl.split(",");
  var mime = arr[0].match(/:(.*?);/)[1];
  var bstr = atob(arr[1]);
  var n = bstr.length;
  var u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], { type: mime });
}

function sendDataUrlViaForm(dataUrl) {
    var formData = new FormData();
    var blob = dataURLToBlob(dataUrl);
    formData.append("file_list", blob, "filename.png"); // "file"은 서버에서 파일을 받을 때 사용할 키 이름입니다.

    // Ajax 또는 Fetch 등을 사용하여 formData를 서버로 전송합니다.
    // 아래는 Fetch API를 사용한 예시입니다.
    fetch("/save", {
        method: "POST",
        body: formData
    })
    .then(response => {
      // 응답 처리
      console.log(response);
      window.location.href = response.url;
    })
    .catch(error => {
      // 오류 처리
    });

}

// Start the camera and video streaming when the window loads
// 1st parameter: Event type
// 2nd parameter: Function to be called when the event occurs
window.addEventListener("load", cameraStart);