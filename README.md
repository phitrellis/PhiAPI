# GPT4API
提供GPT4、GPT3.5、Claude V1等模型的在线统一调用接口
## 1. 接口调用
### 1.1 提问
```
POST http://openai.yige.space/api/data/
参数：
{
  "user": "your key",
  "question": "问题",
  "model": "GPT4",  # 支持 GPT4、GPT35、CLAUDE_V1
  "session": "make a uuid4"
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
轮训下面的接口（建议1s一次），当返回status为2的时候表示已生成答案
```
GET http://openai.yige.space/api/data/{id}/
结果同1.2
```

### 1.3 会话
新建会话时生成一个uuid4，传入1.1中，每次新建会话重新生成即可。

### 1.4 报错
1. 当触发敏感词、问题过长或会话过长的时候status_code为400，且code同为400
2. 当欠费的时候，status_code为401，且code同为401
