
## 1. cloud9 생성
    cloud9 IDE 환경을 생성합니다.

## 2. git clone
	https://github.com/nds-cloud/amazon-personalize-demo-2021

## 3. nginx 설치
```sh
sudo yum install -y nginx
chmod 755 /home/ec2-user
sudo cp /home/ec2-user/environment/amazon-personalize-demo-2021/etc/nginx.conf /etc/nginx

# 설명 : sudo vi /etc/nginx/nginx.conf 

sudo service nginx start
```
## 4. before-페이지 화면
    cloud9 ID를 확인 후 아래 url과 region ID를 알맞게 채워서 호출URL을 완성합니다.
```html
https://<CLOUD9_ID>.vfs.cloud9.<REGION_ID>.amazonaws.com
```


## 5. Amazon S3 bucket 만들기
    - s3 bucket ("nds-personalize-demo-2021") 부분을 개인의 bucket이름에 맞게 수정한 후 S3 bucket policy에 적용합니다. 
```json 
{
"Version": "2012-10-17",
"Id": "PersonalizeS3BucketAccessPolicy",
"Statement": [
    {
        "Sid": "PersonalizeS3BucketAccessPolicy",
        "Effect": "Allow",
        "Principal": {
            "Service": "personalize.amazonaws.com"
        },
        "Action": [
            "s3:GetObject",
            "s3:ListBucket",
            "s3:PutObject"
        ],
        "Resource": [
            "arn:aws:s3:::nds-personalize-demo-2021",
            "arn:aws:s3:::nds-personalize-demo-2021/*"
        ]
    }
    ]
}
```
## 6. 데이터 Input
	event_type을 나중에 api로 필수로 넣어야 하는 항목이긴 하지만, 이번 데모에서는 event_type별 가중치를 별도로 설정하지 않았기 때문에 최초 스키마 생성시 data를 생략하였습니다. 
	path : s3://nds-personalize-demo-2021/data.csv

## 7. 솔루션 생성하기
    AWS Personalize 솔루션 생성

## 8. 캠페인 생성하기
	캠페인 생성
    캠페인 arn주소 복사 
    - ex) arn:aws:personalize:ap-northeast-2:123456789012:campaign/<Campaign_Name>


## 9. 트래커 생성하기 
	트래커 ID 복사 
    - ex) 94002a77-7c35-4325-a0ae-389680d37f45

## 10. nginx fastapi 설치 및 연동
	- venv 및 pip 패키지 설치
```sh
cd /home/ec2-user/environment;
python3 -m venv venv
. /home/ec2-user/environment/venv/bin/activate
cd /home/ec2-user/environment/amazon-personalize-demo-2021
pip install -r requirement.txt
```
	- backend API 기동
```sh
cd /home/ec2-user/environment/amazon-personalize-demo-2021/src/recommend-api
#캡페인 arn주소 수정
vi recommend_api.py 
sh start.sh & 

sudo chmod o+rx /var/log/nginx
cd /home/ec2-user/environment/amazon-personalize-demo-2021/src/events-collector
#트래커 ID 수정
sudo vi events_collector.py 
sh start.sh &
```
	- Python Virtual Environment 비 활성화
```sh
deactivate
```
## 11. IAM Role 생성 및 EC2 연동
	- IAM_Role : personalize_role 생성
	- IAM_Role(personalize_role) - EC2 맵핑 
	- cloud9 설정에서 aws certificate disable 설정

## 12. nginx after 소스로 변경
	- nginx.conf DocumentRoot 경로를 before에서 after로수정
    - 기존: /home/ec2-user/environment/amazon-personalize-demo-2021/src/ecommerce-before
    - 변경: /home/ec2-user/environment/amazon-personalize-demo-2021/src/ecommerce-after
```sh
sudo vi /etc/nginx/nginx.conf 
# before를 after로 변경
sudo service nginx restart
```
