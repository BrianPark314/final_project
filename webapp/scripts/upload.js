const submitBtn = document.getElementById("subbtn");
const fileList = document.getElementById("file_list");
const uploadForm = document.getElementById('drug-image-upload-form');
submitBtn.addEventListener("click", (event) => {
  event.preventDefault();
  if (fileList.value === '') {
    alert("제출할 사진을 먼저 선택해주세요!");
  }
  else {
    uploadForm.submit();
  }
});