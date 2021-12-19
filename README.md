# Unmanned-Store-AI-Security-System
#### 재고 관리와 CCTV 모니터링 자동화를 통해 실시간으로 무인 매장안의 절도 발생을 감지하고<br>매장 주인에게 관련 정보를 통지하는 시스템

## 목차
  - [프로젝트 소개](#프로젝트-소개)
  - [주요 기능](#주요-기능)
  - [시스템 구조](#시스템-구조)
  - [모듈 및 디렉토리](#모듈-및-디렉토리)
  - [실행 방법](#실행-방법)
  - [프로젝트 작성자 및 참조](#프로젝트-작성자-및-참조)
<br>

## 프로젝트 소개
### 시연 예시
|1.정상적인 결제상황|2.도난 발생상황|3.정상적인 결제 및 도난 동시에 발생상황|
|:-:|:-:|:-:|
|![First Image](https://user-images.githubusercontent.com/78855847/146689448-cdf966f1-5873-458c-afb7-904c63baa52c.png?h=600&w=700)|![Second Image](https://user-images.githubusercontent.com/78855847/146689452-721fdd95-d67a-40a0-ae3b-00d8fe1b38a0.png?h=600&w=700)|![First Image](https://user-images.githubusercontent.com/78855847/146689455-e85c9197-bddb-43f5-a833-e9cd005c6384.png?h=600&w=700)|

<br>

### 프로젝트 계획이유
최근 매장을 운영하는 기본 유지보수 비용 중 특히 인건비가 늘어남에 따라  
이에 대한 대비책으로 무인 매장을 선택하는 인구가 늘고 있습니다.  
하지만 사람이 상주하지 않는 무인 매장의 특성 상 절도 범죄에 노출되기 쉽고,  
실제로 무인 매장만을 타겟으로 한 절도범죄가 심각하게 증가하고 있습니다.  
<br>
기존에 무인 매장에서 절도 확인 및 현황을 알기 위해서는 재고와 CCTV를 모두 확인해야 했습니다.  
이 과정에 상당한 노동이 요구되었고, 때문에 사건이 발생하고 시간이 한참 흐른 뒤에야 절도 현황을 파악할 수 있었습니다.  
<br>
이에 재고 갱신과 CCTV 확인에 들어가는 노동을 감소시키고  
실시간 모니터링을 통해 발생한 절도 사건에 빠른 조치를 취할 수 있도록  
재고확인과 CCTV 모니터링을 자동화 하는 시스템을 구현해보았습니다.
<br><br>

## 주요 기능

### 재고 관리 자동화  
  * 로드셀을 통한 무게측정을 통해 선반 위의 물건의 개수를 실시간으로 갱신
  * 상품 정보 데이터베이스에 상품의 무게정보 필요
  * 로드셀은 아래와 같은 형태로 사용
  <img src="https://user-images.githubusercontent.com/78855847/146690310-b4431e40-e7d4-4f7f-be51-bccb7421004e.png" width = "40%" height = "40%">
  
### 실시간 CCTV 모니터링
  1. 카메라는 짧은 주기로 계속 사진을 촬영 
  2. 해당 사진은 Yolo를 통해 객체 검출이 시행됨
  3. 검출 결과 사람이 존재하지 않으면 사진을 삭제하고, 사람이 존재하면 30초간 영상을 촬영
  4. 영상 촬영 후 새로 찍은 사진에 사람이 존재하면 다시 영상을 촬영하고,<br> 사람이 존재하지 않으면 절도 발생 감지 프로세스를 진행
  5. 절도 감지 프로세스의 결과로 이상이 없으면 해당 시간동안 촬영한 영상과 사진을 모두 삭제하고,<br> 절도가 발생되었을 경우에는 촬영한 영상과 사진을 버퍼에 저장
  <img src="https://user-images.githubusercontent.com/78855847/146690445-1e0f1083-2e99-45e2-ad18-80fbf7e3663d.png" width = "50%" height = "50%">
  
### 절도 감지
  * 결재기록 기반 재고정보와 무게측정 기반 재고정보를 각각 따로 관리
  * 매장에서 사람이 검출되지 않을 때, 즉 두 재고정보가 서로 일치하여야 하는 시점에 비교를 진행
  * 비교 후 두 정보가 같이 않을 시 "결재를 하지 않고 물건만 사라진 상황" 즉 절도가 발생했다고 판단

### 도난 내용 푸시알림
  * 버퍼로 설정한 디렉토리를 감시
  * 버퍼 안에 새로운 디렉토리가 생성되면 내부의 파일을 확인하고<br>파일저장이 완료되었다는 시그널을 확인하면 파일을 s3에 업로드
  * AWS SNS를 통해 s3에 업로드된 정보를 매장 주인에게 발송

<br><br>
## 시스템 구조
<p align="center">
  <img src="https://user-images.githubusercontent.com/78855847/146690957-d2a5b362-02c5-4632-a638-f171c6d53918.png" width="65%" />
</p>

  1. 손님의 입장을 카메라가 인지  
  2. 손님이 전자저울을 탑재한 선반에서 물건을 가져감  
  3. 전자저울로 측정된 물건의 재고상태가 무게 측정 기반 재고 정보에 갱신  
  4. 손님이 물건에 대한 결재를 진행  
  5. 결재로 인해 변경된 물건의 재고상태가 결재기록 및 재고 정보에 갱신  
  6. 손님의 퇴장을 카메라가 인지 후 재고 비교 프로세스 실행  
  7. 재고 비교 프로세스는 결제에 기반한 재고정보와 무게 측정에 기반한 재고정보를 비교함으로써 수행  
  8. 절도가 발생되었다고 판단되면 도난 된 상품 정보와 영상, 사진 등을 버퍼에 저장  
  9. 버퍼에 저장된 정보가 AWS S3에 업로드 됨  
  10. AWS S3에 업로드 된 정보가 람다 함수를 통해 AWS SNS에 전달  
  11. 전달된 정보를 AWS SNS에서 매장 주인에게 푸시알람으로 통지  

<br><br>
## 모듈 및 디렉토리
### 디렉토리 안내
 * inventory : 재고 정보와 재고 변동 로그가 저장되는 디렉토리
	* inventory_store.csv 	: store 모듈에 의해 재고 상품의 (상품명, 개수, 가격, 무게)가 기록되는 DB
	* inventory_weight.csv 	: weight 모듈에 의해 재고 상품의 (상품명, 개수, 가격, 무게)가 기록되는 DB
	* store_log.txt 	: store 모듈에 의해 변경된 재고 정보가 기록되는 txt파일
	* weight_log.txt 	: weight 모듈에 의해 변경된 재고 정보가 기록되는 txt파일

* record : 영상과 사진이 저장되는 디렉토리
	- 저장되는 사진과 영상은 해당 파일이 생성된 시간을 이름으로 가짐
* issue_data : 푸시알람으로 전송될 정보가 저장되는 디렉토리
	- 전송될 정보가 저장된 디렉토리는 생성된 시간을 이름으로 가짐

### 모듈 안내
* store.ipynb : 키오스크(결재) 모듈 
 	* inventory_store.csv의 정보를 불러옴
	* 결재 프로세스 진행하면 결과를 inventory_store.csv에 저장 및 store_log.txt에 변동 로그 저장

* weight.ipynb : 저울을 통한 재고 관리 모듈
	* inventory_weight.csv의 정보를 불러옴
	* 무게 측정을 통해 inventory_store.csv에 재고 정보 갱신 및 weight_log.txt에 변동 로그 저장

* camera.ipynb : 영상 촬영 및 도난 감지 모듈
	* original.jpg : (사람이 없을 때 매장 사진)

	* 주기 마다 카메라를 통해 사진을 촬영, 사진에 대한 객체 인식 프로세스 진행
	* 객체인식 결과 사람이 검출될 시 영상을 약20초간 촬영 후 영상 파일 이름 리스트에 저장
	* 사람이 검출되지 않을 경우, 사람이 존재하지 않는다고 판단하고   
	  inventory_store.csv 와 inventory_weight.csv의 정보를 비교(재고 비교)
		* 비교 결과 재고가 다른 경우(도난 발생)
			* 도난에 대한 정보와 해당 시간대의 사진을 issue_data 디렉토리 안에
			  새로운 디렉토리를 만들어 저장(txt파일 1개, jpg 파일 1개)
			* inventory_weight.csv에 맞춰 inventory_store.csv 재고 정보를 갱신 후 event.txt에 기록
			* 영상을 저장하는 리스트를 리셋 -> 절도 상황 발생시 촬영한 영상 영구 저장 
		* 비교 결과 재고가 같은 경우(도난 x)
			* 리스트에 저장된 영상파일들을 모두 삭제 후 리스트 리셋

* s3upload.py & aws 클라우드 : 도난 정보 푸시 알람 모듈 
	* issue_data에 새로운 디렉토리가 생성되는지 2초마다 확인
	* 새로운 디렉토리가 생성된 것 을 확인하면
		* 안에 txt파일 1개와 jpg파일 1개가 있는지 확인 후 없으면 생기길 기다림
		* 안에 txt파일 1개와 jpg파일 1개가 있으면 AWS s3에 업로드
	* s3에 새로운 txt파일과 jpg파일이 업로드 되면 이를 매점 주인의 휴대폰으로 문자 전송(AWS 람다/SNS)

<br><br>
## 실행 방법
### 사전 장비 세팅
1. 로드셀과 hx711을 이용한 간이 저울을 라즈베리파이와 연결 <br>  <img src="https://user-images.githubusercontent.com/78855847/146691543-330789dc-b218-4c2f-9868-c41e81498d4b.png" width = "50%" height = "50%">
2. 라즈베리파이에 카메라 연결
3. 카메라 위치 및 저울 세팅

### 사전 환경 세팅
1. https://github.com/sungjuGit/Pytorch-and-Vision-for-Raspberry-Pi-4B 에서<br>Pytorch, Pytorch Vision 설치에 필요한 wheel 파일을 라즈베리파이에 다운로드
2. `https://github.com/Jeensh/Unmanned-Store-AI-Security-System`를 라즈베리파이에 클론
3. **inventory** 디렉토리안의 csv파일에 상품 데이터를 작성
4. **aws s3**와 **aws sns** 세팅
5. **s3upload.py** 안에 IAM정보 입력

### 시스템 구동 방법
1. **store.ipynb** 실행
2. **weight.ipynb** 실행
3. 전자저울 선반에 상품 진열 
4. **camera.ipynb** 실행
5. **s3upload.py** 실행
6. 테스트 진행

<br><br>
## 프로젝트 작성자 및 참조
### 작성자
  * 컴퓨터공학과 2018110651 신동해
  * 캡스톤 디자인2 프로젝트

### 참조
  * https://aws.amazon.com/
  * https://yhkim4504.tistory.com/13
  * https://github.com/ultralytics/yolov5
  * https://github.com/sungjuGit/Pytorch-and-Vision-for-Raspberry-Pi-4B
