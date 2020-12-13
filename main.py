from requests import get, post
import boto3
from decouple import config
import json

# https://aws.amazon.com/ko/premiumsupport/knowledge-center/build-python-lambda-deployment-package/
# python3 -m pip install requests -t ./
url = config('SLACK_HOOK_URL')
filename = config('FILE_NAME')
bucketname = config('BUCKET_NAME')
my_nickname = config('MY_NICKNAME')
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def get_exp(name):
    got = get(f'https://api.solved.ac/v2/users/show.json?id={name}').json()
    return got['result']['user'][0]['exp']

def ranklist():
    url = 'https://api.solved.ac/v2/ranking/list.json?type=tier&page=%d'
    ls = []
    for i in range(1, 4):
        ls += get(url % i).json()['result']['users']
    return ls


def upload_json(obj):
    return s3_client.put_object(Body=json.dumps(obj).encode('utf-8'), Bucket=bucketname, Key=filename)


def download_json():
    return json.loads(s3.Object(bucketname, filename).get()['Body'].read().decode('utf-8'))


def send_slack(message):
    return post(url, json={'text': message})

def generate_data():
    ls = ranklist()
    idx = None
    for i, user in enumerate(ls):
        if user['user_id'] == my_nickname:
            idx = i
            break
    if idx is None:
        raise RuntimeError('idx not found')

    def tmp(i):
        return [i + 1, ls[i]['user_id'], '{:,}'.format(ls[i]['exp'])]

    return [tmp(i - 2), tmp(i - 1), tmp(i), tmp(i + 1), tmp(i + 2)]


def stringify_data(data):
    mxnum = len(str(data[-1][0]))
    mxlen = len(max((i[1] for i in data), key=len))
    fmt = f'%{mxnum}d. %{mxlen}s - %s'
    return '```' + '\n'.join(fmt % tuple(l) for l in data) + '```'

def main():
    data = generate_data()
    if data != download_json():
        upload_json(data)
        text = stringify_data(data)
        resp = send_slack(text)
        return [resp.status_code, text]
    else:
        return [200, 'EQUAL']


def lambda_handler(event, context):
    try:
        result = main()
        print(result)
        return {
            'statusCode': result[0],
            'body': f'Status code = {result[0]}.\n{result[1]}'
        }
    except Exception as e:
        post(url, json={'text': str(e)})
        raise e


if __name__ == '__main__':
    lambda_handler(None, None)
