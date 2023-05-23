# GPT4API
提供GPT4、GPT3.5、Claude V1等模型的在线统一调用接口

## 1. 获取key
在[https://chat.phitrellis.com](https://chat.phitrellis.com/user)充值购买会员，然后拿到自己的key

## 2. 接口调用
### 2.1 提问
```
POST https://chat.phitrellis.com/api/data
参数：
{
  "user": "your key",
  "question": "问题"
}
```
