# 说明
**使用前请先添加客服，说明使用目的等进行权限申请**
- 平台网址：https://chat.phitrellis.com

# PhiAPI
提供新闻事件抽取、摘要、翻译、文档信息标准化抽取等多种接口及普通聊天对话接口，支持的模型包括：GPT系列、Claude系列、文心一言等

## 1. 接口调用
### 1.1 上传附件
如需上传附近，如PDF、DOCX、MP3等，需要先调用此接口
```
POST http://openai.yige.space/api/usermedia/upload_media/
参数：传入 file 文档及用户 user
具体见 3.1 示例上传
```

### 1.2 提问
```
POST http://openai.yige.space/api/data/
参数：
{
  "user": "your key",
  "question": "问题",
  "question_type": "在线搜索",  # 可以为空
  "model": "GPT4",  # 对话所用的模型，任选一个，具体支持模型见2. 支持模型
  "session": "make a uuid4"  # 如果问答需要支持上下文，则传入一个自己生成的uuid4，并在后续传入此同一个值，当开启新的会话的时候传入新uuid4，如果不需要支持上下文，则无需传入
}
```
### 1.3 返回
```
{
    "status": "OK",
    "code": 201,
    "data": {
        "id": "4c9782af-8731-4074-b2dd-739575f83564",
        "status": 0,
        "answer": null,
        "session": "uuid4"
    }
}
```
重点关注 id,status,answer

### 1.4 取结果
轮询下面的接口（建议1s一次），当返回status为2的时候表示已生成答案
```
GET http://openai.yige.space/api/data/{id}/
结果同1.2
```

### 1.5 会话
新建会话时生成一个uuid4，传入2.1的session中，每次新建会话重新生成即可。

### 1.6 报错
1. 当触发敏感词、问题过长或会话过长的时候status_code为400，且code同为400
2. 当欠费的时候，status_code为402，且code同为402

### 2. 支持模型
GPT5
O1
O3
O3_PRO
CODEX
OPUS
SONNET
GEMINI_PRO
DEEPSEEK
DEEPSEEK_THINK

## 3. 示例

### 3.1 上传

```python
path = '/your/path/to/file'
response = requests.post('http://openai.yige.space/api/usermedia/upload_media/?user={用户标识}', files={'file': open(path, 'rb')})
print(response.json())
# {'status': 'OK', 'code': 200, 'data': 'xxx'}
# 拿到 data 中的链接，下一步提问时传入使用
link = response.json()['data']
```

### 3.2 发送问题
```python
import time
import requests

## 如果有上传文档，则使用文档链接拼装 config 传入
link = 'xxx'  # 3.1 上传文档后返回的链接
config = {'link': [{'url': link, 'name': 'xxx.txt'}]}

data = {
    # 'session': 'uuid v4',
    'user': '{用户标识}',
    'question': 'hi',
    'config': config,  # 如果需要上传文档，则传入 config
    'model': 'GPT5'
}
response = requests.post('http://openai.yige.space/api/data/', json=data)  # 提问
print(response.json())
if response.status_code == 200:  # 判断是否正常返回
    id = response.json()['data']['answer_id']  # 获取本次提问返回的 answer id
    while True:
        time.sleep(1)  # 1s 轮询一次，等待结果
        response = requests.get(f'http://openai.yige.space/api/answer/{id}/?user={用户标识}')  # 查询结果
        print(response.json())
        if response.status_code == 200 and response.json()['data']['status'] == 2:  # 正常处理完毕
            answer = response.json()['data']['answer']  # 取出结果
            print(answer)
            break
```
