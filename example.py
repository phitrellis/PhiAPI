import time
import requests

data = {
    'session': 'uuid v4',
    'user': 'your token',
    'question': 'hi',
    'model': 'GPT35'
}
response = requests.post('http://openai.yige.space/api/data/', data=data)  # 提问
if response.status_code == 200:  # 判断是否正常返回
    id = response.json()['data']['id']  # 获取本次提问 id
    while True:
        time.sleep(1)  # 1s 轮询一次，等待结果
        response = requests.get(f'http://openai.yige.space/api/data/{id}/')  # 查询结果
        if response.status_code == 200 and response.json()['data']['status'] == 2:  # 正常处理完毕
            answer = response.json()['data']['answer']  # 取出结果
            print(answer)
            break
