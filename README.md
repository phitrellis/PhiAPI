# GPT4API
提供GPT4、GPT3.5、Claude V1 100K 等模型的在线统一调用接口
## 1. 接口调用
### 1.1 提问
```
POST http://openai.yige.space/api/data/
参数：
{
  "user": "your key",
  "question": "问题",
  "model": "GPT4",  # 对话所用的模型，支持 GPT4、GPT35、CLAUDE_V1，三者任选一个
  "session": "make a uuid4"  # 如果问答需要支持上下文，则传入一个自己生成的uuid4，并在后续传入此同一个值，当开启新的会话的时候传入新uuid4，如果不需要支持上下文，则无需传入
}
```
### 1.2 返回
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

### 1.2 取结果
轮询下面的接口（建议1s一次），当返回status为2的时候表示已生成答案
```
GET http://openai.yige.space/api/data/{id}/
结果同1.2
```

### 1.3 会话
新建会话时生成一个uuid4，传入1.1中，每次新建会话重新生成即可。

### 1.4 报错
1. 当触发敏感词、问题过长或会话过长的时候status_code为400，且code同为400
2. 当欠费的时候，status_code为401，且code同为401

## 2. 示例
```python
data = {
    'session': 'uuid v4',
    'user': 'your token',
    'question': 'hi'
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
```
