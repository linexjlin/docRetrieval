from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
import os

scenes_path = "scenes"
index_path = "indexes"

#default_model_name = "all-MiniLM-L6-v2"
default_model_name = "moka-ai/m3e-base"


class DocSearch:
    def __init__(self, model_name=default_model_name, data_path=scenes_path, persist_directory=".chroma"):
        self.model_name = model_name
        self.data_path = data_path
        self.persist_directory = persist_directory
        self.embedding_function = SentenceTransformerEmbeddings(model_name=self.model_name)
        self.text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
        #self.loader = TextLoader(self.data_path)
        self.db = None

    def load_to_db(self):
        db_file = f"{self.persist_directory}/chroma.sqlite3"
        # check if db_file exist 
        if os.path.exist(db_file):
            self.db = Chroma(persist_directory=self.persist_directory, self.embedding_function)
            return
        
        self.loader = DirectoryLoader(self.data_path, glob="**/*.txt", loader_cls=TextLoader)
        documents = self.loader.load()
        print(f"reload documents from {self.data_path}")
        # filter the document.page_content not empty document in documents
        documents = [document for document in documents if document.page_content != ""]
        if len(documents)>0:
            docs = self.text_splitter.split_documents(documents)
            self.db = Chroma.from_documents(docs, self.embedding_function, persist_directory=self.persist_directory)

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
            self.data[scene_id].load_to_db()
        return self.data[scene_id]
    
