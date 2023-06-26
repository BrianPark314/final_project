### 경구 약제 이미지 데이터를 통한 약제 성분 분석 
배경 : 평소에 약을 먹는 소비자들이 약에 대한 성분 정보를 쉽게 알지 못함 특히 약의 종류가 많아지면 이를 분석하기가 쉽지 않다.
목표 : 경구약제 약품식별 결과를 안내하고 피드백 할 수 있는 AI 서비스 모델 구축 
 
#### 1.1 데이터 수급 
경구 약제 이미지 데이터(단일,조합경구약 분류 / 전문,일반 분류 / 약 성분 라벨)
- https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=576

#### 1.2 데이터 처리
- 4.5TB 크기의 데이터 추후 저장 및 처리 방법 논의
- 단일 약제 객체 이미지의 약부분만 테두리를 추출하고 나머지는 padding으로 채워 학습
#### 1.3 데이터 제공
- 

#### 질문 리스트
- 주제에 대한 데이터 수급이 가능한가 ? 
-> 찾아본 데이터는 무료로 다운이 가능
- 분석 / 추천을 하는데 적합한 알고리즘이 확인 되었는가 ?
-> 
- 서비스 시나리오가 기간내 구현이 가능한 수준인가 ?
-> 모델 학습에 큰 문제만 없다면 시간내 구현 가능할것으로 예상 
- 모델이 필요한 경우 이미 공개된 모델이 확인/확보 되었는가? 
-> 추가 조사 필요