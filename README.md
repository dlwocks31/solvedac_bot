# solvedac_bot
자신의 [solved.ac](https://solved.ac/) 랭킹 변동이 있을 때마다 슬랙으로 알림을 주는 봇을 제어하는 AWS Lambda함수를 만듭니다.
```
105.   some_name - 232,582,384
106.      name_2 - 231,951,046
107. MY_NICKNAME - 230,218,173
108.         XXX - 228,207,852
109.         YYY - 227,613,521
```
위와 같이 등수 - 닉네임 - 경험치가 포함된 메세지를 변동될 때마다 보내줍니다.

구체적인 알람 주기나 트리거는 Lambda단에서 Cloudwatch Event나 API Gateway를 추가해야 합니다.

Github Action을 통한 간단한 CD가 구축되어 있습니다.

## How To Use
테스트해보진 않았지만 아마 아래와 같이 설정하면 충분할 것입니다.
### On Local
1. 슬랙 Workspace를 만들거나 기존 Workspace에서 hook url을 만든다. `https://hooks.slack.com/services/TXXXX1236/BYYYY4569/Iqwertyuiopy` 와 같은 형태.
1. .env 파일 설정 (하단 Variables 항목 참고)
2. S3관련 권한이 있도록 AWS CLI를 설정한다.
3. `python main.py`

### On Lambda
1. 위의 On Local을 완료한다.
2. cd.yml의 jobs.build.steps[-1].with.function_name에 해당하는 함수를 Lambda에 만든다. (TODO: 이거 미리 만들어놔야 하는건가?)
3. 해당 Repo를 Fork한 후 Repo Secret을 설정한다. 설정한 AWS계정에는 S3, Lambda관련 권한이 필요하다.
4. `git push`
5. Actions탭과 AWS Console에서 Lambda가 정상 배포되는 것을 확인
6. .env 파일 설정한것과 같이 Lambda의 Environment Variable에 추가 (하단 Variables 항목 참고)
7. Cloudwatch Event나 API Gateway를 설정해 Lambda의 트리거 설정.

## Warning
현재 코드는 MY_NICKNAME에 해당하는 유저가 298등 안에 들어있을 것을 가정합니다.

## Variables
환경변수와 Repo Secret를 설정해야 합니다.
설정해야 할 환경변수:(로컬에서는 .env 파일에, Lambda에서는 함수 설정에)
- SLACK_HOOK_URL: 슬랙 메세지를 보낼 Hook url
- FILE_NAME: 전에 보낼 메세지를 S3에 저장하는데, 이때 사용할 파일 이름
- BUCKET_NAME: S3 Bucket이름
- MY_NICKNAME: 사용자의 BOJ 닉네임

설정해야할 Repo Secret:
- AWS_ACCESS_KEY_ID
- AWS_REGION
- AWS_SECRET_ACCESS_KEY
