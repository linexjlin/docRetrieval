# 文档检索API

## API 1: 上传文档

### Endpoint
```
POST /api/upload/{scene}/{path}
```

### 请求参数
* `scene` (必填): 文档所属的场景名称。
* `path` (必填): 文档在场景中的路径。
* `file` (必填): 要上传的文档文件。

### 返回数据
* `message`: 上传状态的字符串。

### 示例
```
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@file.txt"  http://127.0.0.1:6080/api/upload/test5/docs
```

### 预期返回数据
```json
{
    "message": "File file.txt uploaded to test5/docs"
}
```

## API 2: 搜索文档

### Endpoint
```
GET /api/{scene}/search
```

### 请求参数
* `scene` (必填): 要搜索的场景名称。
* `q` (必填): 要搜索的查询字符串。

### 返回数据
* `page_content`: 匹配文档的内容。
* `source`: 匹配文档的来源。
* `score`: 匹配文档的相关性得分。

### 示例
```
curl http://127.0.0.1:6080/api/scene1/search?q=python
```

### 预期返回数据
```json
[
    {
        "page_content": "Python是一种解释型、高级、通用型编程语言。",
        "source": "file.txt",
        "score": 0.8
    },
    {
        "page_content": "Python是数据分析和机器学习中常用的编程语言。",
        "source": "file2.txt",
        "score": 0.6
    }
]
```