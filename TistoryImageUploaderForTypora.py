import os
import sys
import json
import requests
from configparser import ConfigParser

import browser_cookie3

TSSESSION = 'TSSESSION'
config_path = f'{os.path.dirname(sys.argv[0])}/config.ini'

config = ConfigParser()

if len(sys.argv) == 1:
    url_input = input("티스토리 블로그 주소를 입력하세요. (예: yourblogname.tistory.com)\n")
    
    config['urls'] = {
        'blogURL': url_input
    }

    token = ""
    cookies = browser_cookie3.chrome(domain_name=".tistory.com")
    for cookie in cookies:
        if cookie.name == TSSESSION:
            token = cookie.value
    config['tokens'] = {
        TSSESSION: token
    }

    with open(config_path, 'w') as config_file:
        config.write(config_file)
    
    print("블로그 주소와 로그인 정보를 config.ini에 저장했습니다. 이제 Typora Custom 이미지 업로더로 사용할 수 있습니다.")
    input()
    sys.exit()

blog_url = ""
token = ""
if os.path.exists(config_path):
    config.read(config_path)
    blog_url = config['urls']['blogURL']
    token = config['tokens'][TSSESSION]
else:
    print("[Error] Cannot find config file. Run file directly and set blog url.")
    sys.exit()

def upload(data):
    url = f"https://{blog_url}/manage/post/attach.json"
    files=[
        ('file',('img.png', data, 'image/png'))
    ]
    headers = {
      'Cookie': f'{TSSESSION}={token}'
    }
    response = requests.request("POST", url, headers=headers, files=files)

    result = json.loads(response.text)
    image_url = result["url"]
    print(image_url)

for path in sys.argv[1:]:
    with open(path, 'rb') as file:
        try:
            upload(file)
        except:
            print("[Error] Failed to upload. Check blog url, internet connection and Tistory login status.")
        