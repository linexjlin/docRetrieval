from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
import os

from dotenv import load_dotenv
load_dotenv()

default_model_name = os.getenv("EMB_MODEL") if os.getenv("EMB_MODEL") else "all-MiniLM-L6-v2"

scenes_path = "scenes"
index_path = "indexes"

class DocSearch:
    def __init__(self, model_name=default_model_name, data_path=scenes_path, persist_directory=".chroma"):
        self.model_name = model_name
        self.data_path = data_path
        self.persist_directory = persist_directory
        self.embedding_function = SentenceTransformerEmbeddings(model_name=self.model_name)
        self.text_splitter = CharacterTextSplitter(chunk_size=600, chunk_overlap=200)
        #self.loader = TextLoader(self.data_path)
        #self.db = None
        self.db = Chroma(embedding_function=self.embedding_function,persist_directory=self.persist_directory)
        

    def load_all(self):
        # remove index?
        self.loader = DirectoryLoader(self.data_path, glob="**/*.txt", loader_cls=TextLoader)
        documents = self.loader.load()
        print(f"reload documents from {self.data_path}")
        # filter the document.page_content not empty document in documents
        documents = [document for document in documents if document.page_content != ""]
        if len(documents)>0:
            docs = self.text_splitter.split_documents(documents)
            self.db = Chroma.from_documents(docs, self.embedding_function, persist_directory=self.persist_directory)

    def add_document(self,doc_path):
        print(f"delete {doc_path}")
        self.del_document(doc_path)

        print(f"embeding {doc_path}")
        loader = TextLoader(doc_path)
        documents = loader.load()
        docs = self.text_splitter.split_documents(documents)

        self.db.add_documents(docs)

        self.db.persist()

    def del_document(self,doc_path):
        self.db.delete(where=doc_path)

    def list_documents(self):
        print(self.db.get()["metadatas"])
        return self.db.get()["metadatas"]

    def query(self, question):
        if self.db is None:
            #raise ValueError("Database not loaded. Call load_to_db() before querying.")
            return []

        docs = self.db.similarity_search_with_score(question)
        return docs

"""
search = DocSearch(data_path="docs/md/eng.txt",persist_directory=".chroma3")
search.load_to_db()

question = "What is Faiss?"
results = search.query(question)
print(results)
"""

class DocSearchManage:
    def __init__(self):
        self.data = {}

    def new(self, scene_id):
        if scene_id not in self.data:
            self.data[scene_id] = DocSearch()
        return self.data[scene_id]

    def get(self, scene_id):
        if scene_id not in self.data:
            path = f"{scenes_path}/{scene_id}"
            os.makedirs(path, exist_ok=True)
            data_path=f"{scenes_path}/{scene_id}"
            print(data_path)
            self.data[scene_id] = DocSearch(data_path=data_path, persist_directory=f"{index_path}/chroma.{scene_id}")
        return self.data[scene_id]
    
