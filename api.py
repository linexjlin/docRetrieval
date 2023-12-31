import os
from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv

from doc_search import DocSearchManage

scenes_path = "scenes"

doc_manager = DocSearchManage()

app = FastAPI()

@app.post("/api/documents/{scene}/{path}")
async def create_upload_file(scene: str, path: str, file: UploadFile = File(...)):
    storage_path = f"{scenes_path}/{scene}/{path}"
    user_path = f"{scene}/{path}"
    os.makedirs(storage_path, exist_ok=True)  # 创建路径（如果不存在）

    # 保存上传的文件
    save_path = os.path.join(storage_path, file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())
        dcs = doc_manager.get(scene)
        f.close()
        dcs.add_document(save_path)

    return {"message": f"File {file.filename} uploaded to {user_path}"}

@app.delete("/api/documents/{scene}")
async def create_upload_file(scene: str,file: str):
    dcs = doc_manager.get(scene)
    docs = dcs.del_document(file)

    return {"message": f"File {file} deleted"}

@app.get("/api/documents/{scene}")
async def create_upload_file(scene: str):
    dcs = doc_manager.get(scene)
    docs = dcs.list_documents()
    return docs

@app.get("/api/{scene}/search")
async def search(scene: str,q: str):
    dcs = doc_manager.get(scene)
    results = dcs.query(q)
    json_list = []
    for result in results:
        print(result)
        json_list.append({"page_content": result[0].page_content, "source": result[0].metadata['source'],"socre":result[1]})
    return json_list