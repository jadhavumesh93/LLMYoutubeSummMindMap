import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from pathlib import Path
from dotenv import load_dotenv

class LLMEmbeddings:
    def __init__(self, video_id = None, video_url = None, text = None, new_video = True, vectore_store_action = 0):
        load_dotenv()
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.video_id = video_id
        self.video_url = video_url
        self.text = text
        self.vectore_store_action = vectore_store_action
        self.new_video = new_video
        
        # File path resolution
        current_file = Path(__file__).resolve()
        parent_dir = current_file.parent.parent
        self.vector_db_path = os.path.join(parent_dir, "yt_db")
        
    def generate_documents(self):
        try:
            doc = Document(
                page_content=self.text.strip(),  # This is the key - page_content is required!
                metadata={
                    "video_id": self.video_id,
                    "source": self.video_url,
                    "title": "YouTube Video"
                }
            )
            
            return ("success", doc)
        except Exception as ex:
            print(f"{ex}")
            return ("error", ex)
        
    def generate_chunks(self, doc : Document):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=100
            )
            chunks = text_splitter.split_documents([doc])  # Pass as list

            print(f"✅ Created {len(chunks)} chunks")
            print(f"✅ First chunk type: {type(chunks[0])}")
            print(f"✅ First chunk has page_content: {'page_content' in dir(chunks[0])}")
            
            return ("success", chunks)
        except Exception as ex:
            print(f"{ex}")
            return ("error", ex)
        
    def generate_embeddings(self):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
            
            return ("success", embeddings)
        except Exception as ex:
            print(f"{ex}")
            return ("error", ex)
    
    def generate_vectors_storage(self, embeddings, chunks = None):
        try:
            if(self.new_video):
                self.check_vector_db_exist()
                if(self.vectore_store_action == 1):
                    vectorstore = Chroma.from_documents(
                        documents=chunks,  # Now these are proper Document objects
                        embedding=embeddings, 
                        persist_directory=self.vector_db_path + "/yt_db"
                    )
                    vectorstore.persist()
                else:
                    vectorstore = Chroma(
                        persist_directory=self.vector_db_path + "/yt_db",
                        embedding_function=embeddings
                    )
                    vectorstore.add_documents(chunks)
                    vectorstore.persist()
            else:
                vectorstore = Chroma(
                    persist_directory=self.vector_db_path + "/yt_db",
                    embedding_function=embeddings
                )
            return ("success", vectorstore)
        except Exception as ex:
            print(f"{ex}")
            return ("error", ex)
        
    def check_vector_db_exist(self):
        vector_db_path = Path(self.vector_db_path)
        if(vector_db_path.exists() and vector_db_path.is_dir()):
            self.vectore_store_action = 1
        else:
            self.vectore_store_action = 2
    
    def process(self):
        if(self.new_video):
            (status, doc_res) = self.generate_documents()
            if(status == "error"):
                return (status, doc_res)
            
            (status, chunk_res) = self.generate_chunks(doc_res)
            if(status == "error"):
                return (status, chunk_res)
            
            (status, emb_res) = self.generate_embeddings()
            if(status == "error"):
                return (status, emb_res)
            
            (status, vec_res) = self.generate_vectors_storage(embeddings=emb_res, chunks=chunk_res)
            return (status, vec_res)
        else:
            (status, emb_res) = self.generate_embeddings()
            if(status == "error"):
                return (status, emb_res)
            
            (status, vec_res) = self.generate_vectors_storage(embeddings=emb_res)
            return (status, vec_res)