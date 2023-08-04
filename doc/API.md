# DocRetrieval

## API 1: Upload Documents

### Endpoint
```
POST /api/upload/{scene}/{path}
```

### Request
* `scene` (required): The name of the scene to which the document belongs.
* `path` (required): The path of the document within the scene.
* `file` (required): The file to be uploaded.

### Response
* `message`: A string indicating the status of the upload.

### Example
```
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@file.txt"  http://127.0.0.1:6080/api/upload/test5/docs
```

### Expected Response
```json
{
    "message": "File file.txt uploaded to scene1/docs"
}
```

## API 2: Search Documents

### Endpoint
```
GET /api/{scene}/search
```

### Request
* `scene` (required): The name of the scene to search within.
* `q` (required): The query string to search for.

### Response
* `page_content`: The content of the matching document.
* `source`: The source of the matching document.
* `score`: The relevance score of the matching document.

### Example
```
curl http://127.0.0.1:6080/api/scene1/search?q=python
```

### Expected Response
```json
[
    {
        "page_content": "Python is an interpreted, high-level, general-purpose programming language.",
        "source": "file.txt",
        "score": 0.8
    },
    {
        "page_content": "Python is a popular programming language for data analysis and machine learning.",
        "source": "file2.txt",
        "score": 0.6
    }
]
```
