document.addEventListener("DOMContentLoaded", () => {
    new App();
  })
  
  class App {
    constructor() {
  
      const video = document.querySelector("#videoElement");
  
      if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then( (stream) => { // function 의 this와 화살표 함수의 this 가 다름
            video.srcObject = stream;
          })
          .catch(function (error) {
            console.log("Something went wrong!");
            console.log(error);
            return;
          });
      }
  
      video.addEventListener( "loadedmetadata", () => {
        window.requestAnimationFrame(this.draw.bind(this));
      });
    }
  
    draw(t) {
  
      window.requestAnimationFrame(this.draw.bind(this));
      
      const canvas = document.querySelector("#mirrored");
      const video = document.querySelector("#videoElement");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
  
      const ctx = canvas.getContext('2d');
      ctx.translate(video.videoWidth, 0);
      ctx.scale(-1,1);
      ctx.drawImage(video, 0, 0, 
          video.videoWidth, 
          video.videoHeight);  
      
    }
  }