# PhiAPI
提供新闻事件抽取、摘要、翻译等多种接口及普通聊天对话接口，模型包括：GPT4、GPT3.5、Claude V1 100K

## 1. 接口列表
1. [通用对话](#21-提问)
2. 新闻撰写
3. 新闻事件提取
4. 摘要
5. 实体抽取
6. 数学计算（函数绘图、方程求解、微积分、线性代数）
7. 在线搜索与总结
8. 总结
9. 翻译
10. 画图
11. JSON标准化和错误修正
12. 文档错别字检测
13. 文献信息抽取（标题、作者、摘要、关键字等）
14. 文献翻译、润色
15. 地址解析
16. 生成代码

## 2. 接口调用
### 2.1 提问
```
POST http://openai.yige.space/api/data/
参数：
{
  "user": "your key",
  "question": "问题",
  "question_type": "在线搜索",  # 可以为空
  "model": "GPT4",  # 对话所用的模型，支持 GPT4、GPT35、CLAUDE_V1，三者任选一个
  "session": "make a uuid4"  # 如果问答需要支持上下文，则传入一个自己生成的uuid4，并在后续传入此同一个值，当开启新的会话的时候传入新uuid4，如果不需要支持上下文，则无需传入
}
```
### 2.2 返回
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

### 2.3 取结果
轮询下面的接口（建议1s一次），当返回status为2的时候表示已生成答案
```
GET http://openai.yige.space/api/data/{id}/
结果同2.2
```

### 2.4 会话
新建会话时生成一个uuid4，传入1.1中，每次新建会话重新生成即可。

### 2.5 报错
1. 当触发敏感词、问题过长或会话过长的时候status_code为400，且code同为400
2. 当欠费的时候，status_code为401，且code同为401

## 3. 示例
```python
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
```
