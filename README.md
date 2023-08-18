<style>
  .button {
  background-color: #555555; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}
</style>

<div align=center><h1>ENCORE PLAYDATA FINAL PROJECT</h1>
 <h3>딥러닝 기반 경구약제 이미지 인식 및 정보 제공 서비스</h3>
</div>

<div align=center><h2>TEAM F4</h2></div>
<div align=center><h3>박기영 강호정 서덕원 유준선</h2>

  박기영(팀장) <br>
  개발 및 기획 총괄, 데이터 파이프라인 구축, 벡엔드(main)backend <br>
  강호정 <br>
  image 전처리 , 외부 정보 관리 및 전처리 , backend  ,frontend(sub) <br>
  서덕원 <br>
  model 성능 개선 , image 전처리 , model 학습 <br>
  유준선 <br>
  frontend , json data -> csv 변환 , data전처리

</div>

<div align=center><h2>📚 STACKS</h2></div>

<div align=center> 
  <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> 
  <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
  <img src="https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white"> 
  <img src="https://img.shields.io/badge/js-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 
  <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=black"> 
  <img src="https://img.shields.io/badge/bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=black"> 
  <br>
  
  <img src="https://img.shields.io/badge/google Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"> 
  <img src="https://img.shields.io/badge/google colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white"> 
  <img src="https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"> 
  <img src="https://img.shields.io/badge/yolov5-00FFFF?style=for-the-badge&logo=yolo&logoColor=white">
</div>

<div align=center><h2>INTRODUCTION TO PRODUCT</h2>
  <button href="https://www.canva.com/design/DAFqcupnsGU/9FgB-cWTKufkZOWAvJNH9g/view?utm_content=DAFqcupnsGU&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink" class="button">Link to Presentation</button>
</div>



## 주제 설명 
### 선정 배경 
1. 꾸준히 약을 복용하는 사람들은 약국에서 파는 일반의약품을 먹어도 되는지 잘 모름
2. 중·장년층들은 노화에 따라복용하는 약이 점점 많아짐
3. 여러가지 약을 한번에 보관하는 경우도 흔하므로 중장년층의 약물 오용 방지가 요구됨

### 솔루션 및 목표 
- 전문의약품과 일반의약품 데이터셋을 활용한 ‘이미지분류 모델’ 생성
- 사진을 찍었을 때 혹은 갖고 있는 사진을 넣었을 때 어떤 약인지 분류하거나 약의 성분을 나타내주는 서비스 구현
- 사용자가 사진을 찍거나 업로드하면 복용하면 안되는 약이 있는 경우 어떤 약인지 알려주는 웹앱 서비스 구현 
-> 사진 한장으로 약에대한 정보 , 복용 주의 정보를 쉽게 알 수 있는 서비스 구현 


## 주요 과정 
preprocessing and model training
- utils , engine 등 common 함수 module 화
- bounding box 처리 (gasussain blur , contour 등)
- ai hub에서 다운받은 원본 파일 압축 해제 , 디렉토리 생성 , 이미지 이동 , 레이블 생성 자동화
- 이미지 정보(json) 을 적극 활용해 이미지 최적의 학습 데이터 생성 
- yolov5 base gcs->colab을 통한 model training 
- model 최적화 

front backend 
- html , js , css , fastapi를 활용해 서비스 웹앱 구현


## issue정리 
### 1. preprocessing and model 
#### 1.1)bounding box 처리 and model 학습 issue
- 자체적으로 bounding box를 추출하는 작업을 하기위해 opencv gaussian blur , countour작업등을 해서 bounding box추출 후 test  
issue : bouding box 가 모양에 따라 알약 bounding box를 제대로 추출 못하는 문제가 생김 
issue : 배경 noise 처리 문제

try1:  데이터에 주어진 json 파일 내 bouding box 좌표를 적극 활용하도록 변경  
issue : yolov5 label 형식에 맞춰줘야 하는 문제(x,y자체가 yolov5일때 상대 좌표이므로)

try2: 상대좌표 기준에 맞게 비율 변경 후 640*640 crop 이미지를 demo model에 학습을 시킴 (칠판 참고)
issue : 상대좌표가 1이 넘는 오류가 발생 

try3 : 이미지를 절반으로 resize 1/2 and resize 한거에 맞게 bouding box 좌표 변경 후 학습 
issue : gcs -> cloab mount시 속도 저하 

try4 : cloab 가상머신상에서 진행할시
iusse : colab 가상머신 용량 한정 issue 

try5: bounding box + padding 20 만큼만 crop 후 학습 
issue : 50epoch model 학습시 23epoch까지 하고 멈춰버리는 문제(colab bug) 



#### 1.2) csv 전처리 issue  
- 데이터 확보 및 json 정보 csv 파일 변환 
try 1: json image 정보 csv 파일 형태로 변환 module 화
issue : csv 데이터 자체 이상치 , 비정규화 문제 / 필요없는열이 많은 문제

try 2 : 데이터 전처리 (정규화 , 이상치제거 , 결측치많은열 제거 , 필요없는열 제거)
issue : issue 서비스를 구현하기에 필요한 정보가 부족

try 3 : 추가 데이터 확보 및 품목코드를 기준으로 csv merge 시도
- 관련 데이터 : 병용금지약물 , 중복주의약물 , 약에대한세부정보 data 
issue : 원본 데이터랑 겹치지 않는 약이 많았음  

try 4 : 사용자가 업로드 또는 촬영한 이미지에 대한 정보에만 매칭시키는 logic 구현 
issue : 겹치지 않는 데이터가 많은 문제(한계점)


------------------------------------------------------------------------------------------------------------------------------

### 2)데이터 용량 문제 + 연동 문제 (4.4TB)
- 데이터를 다운받고 압축을 풀고 하는 과정 시도
main issue : 데이터 용량 issue로 local에 데이터를 다운하는것이 불가능
try1 : GCS상에 데이터를 다운 받으려 시도 

issue : ai hub 자체방식(innor ixes) 이 GCS로 바로 가는 방법이 없는 문제
try2 : 데이터를 외장하드에 다운 받는 방법 선택 

issue : 외장하드에서 압축을 푸는 과정 , 이미지를 자르는 과정이 시간적 문제 생김   , python unzip bug로 인해 파일 누락 문제 
try3 : shell code 를 활용해 외장하드(local)에서 GCS상으로 압축을 자동으로 풀고 crop해주는 process 구현(gcs i/o shell scripts 명령어 사용 필수)
issue : GCS upload시 바우처문제로 비용이 발생해 20% 하고 중단 

try4 : 20%(92만장) 이미지 데이터로  라벨링 및 BBOX를 추출해야하는 작업을 진행
issue : 전체 데이터셋(250만 row)에서 92만장과 일치하는 항목만 추출했으나 속도 저하 문제 발생 
issue : label 110만개 이상 생성시 속도 저하현상발생

try5: 110만개씩 끊어서 label 생성 

issue : 이미지 및 라벨 데이터 180만개 학습 시도시 colab gpu cuda out of memory 발생
try6 : 이미지 데이터 라벨당 200개씩 비율 맞춰 42만개로 개수 줄여줌

issue : 배치사이즈 128,64 시도시 colab gpu cuda out of memory 발생
issue : yaml 파일 그대로 사용하여 학습시도시 학습률0% 발생
try7 : 이미지 라벨 새로추출 및 yaml 재생성 후 학습 시도, 배치사이즈 32까지줄여서 학습 진행


- 데이터 용량 줄이기 시도
main issue : unzip -> crop -> GCS 과정에 데이터 크기가 여전히 압도적으로 큼 
try1 : 이미지를 중앙 기준으로 640*640크기로 바꿔 저장 (용량 1/10정도로 줄음)
try2 : resize 1/2 
try3 : bouding box + padding 20

---------------------------------------------------------------------------------------------------------

### 3) backend & frontend 구축 문제 
- 사진을 업로드 또는 촬영하면 best model 을 타고 화면상에 detection image  + image information 구현 시도 
main issue : backend tool 활용 선택 문제 
try1 : django 를 활용한 yolov5 서비스 구현 시도 
issue : 익숙하지 않은 tool과 참고 reference자료 부족으로 변경 
try2 : python web library streamit 을 활용한 backend 서비스 구현 시도 
issue : 서비스는 구현 되었으나 frontend 와 연결 과정에서 서버를 2개 open해야 한다는 문제 생김(유지 보수면 비효율적)
try3 : flask를 활용해 image upload detection  , caputre and detection 부분 구현성공 
issue : 4차 멘토링을 통한 피드백으로 fast api가 더 좋겠다는 평가를 받음 
try4 : fast api를 활용해 backend 구현 (camera capture detection , image upload detedction)
issue : 요청받은 이미지를 fetch로 전달하는 과정에서 get이 안되는 issue 발생 (code수정완료)
try5 : frontend 수정 및 docker 환경에서 실행 가능 하도록 구현 

