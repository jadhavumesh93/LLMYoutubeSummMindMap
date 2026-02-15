import os
import time
from pathlib import Path
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


class LLMEmbeddings:

    def __init__(self, video_id=None, video_url=None, video_title=None, text=None):
        load_dotenv()

        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.video_id = video_id
        self.video_url = video_url
        self.video_title = video_title
        self.text = text

        # ✅ Persistent DB path
        current_file = Path(__file__).resolve()
        parent_dir = current_file.parent.parent
        self.vector_db_path = os.path.join(parent_dir, "yt_db")

    # --------------------------------------------------
    # DOCUMENT CREATION
    # --------------------------------------------------
    def generate_documents(self):
        try:
            doc = Document(
                page_content=self.text.strip(),
                metadata={
                    "video_id": self.video_id,
                    "source": self.video_url,
                    "title": self.video_title,
                    "indexed_at": time.time()
                }
            )
            return ("success", doc)

        except Exception as ex:
            return ("error", ex)

    # --------------------------------------------------
    # CHUNKING
    # --------------------------------------------------
    def generate_chunks(self, doc: Document):
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )

            chunks = splitter.split_documents([doc])

            # ✅ Ensure metadata propagates
            for chunk in chunks:
                chunk.metadata["video_id"] = self.video_id
                chunk.metadata["source"] = self.video_url

            return ("success", chunks)

        except Exception as ex:
            return ("error", ex)

    # --------------------------------------------------
    # EMBEDDINGS
    # --------------------------------------------------
    def generate_embeddings(self):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=self.google_api_key
            )
            return ("success", embeddings)

        except Exception as ex:
            return ("error", ex)

    # --------------------------------------------------
    # CHECK IF VIDEO EXISTS (FAST METADATA QUERY)
    # --------------------------------------------------
    def video_exists(self, embeddings):
        try:
            if not Path(self.vector_db_path).exists():
                return False

            vectordb = Chroma(
                persist_directory=self.vector_db_path,
                embedding_function=embeddings
            )

            result = vectordb.get(
                where={"video_id": self.video_id},
                limit=1
            )

            return len(result["ids"]) > 0

        except Exception as ex:
            print(f"Metadata check error: {ex}")
            return False

    # --------------------------------------------------
    # LOAD / UPDATE VECTOR STORE
    # --------------------------------------------------
    def generate_vectorstore(self, embeddings, chunks=None):
        try:
            os.makedirs(self.vector_db_path, exist_ok=True)

            vectordb = Chroma(
                persist_directory=self.vector_db_path,
                embedding_function=embeddings
            )

            # ✅ Add only if new chunks provided
            if chunks:
                ids = [
                    f"{self.video_id}_{i}"
                    for i in range(len(chunks))
                ]

                vectordb.add_documents(
                    documents=chunks,
                    ids=ids
                )

                vectordb.persist()

            return ("success", vectordb)

        except Exception as ex:
            return ("error", ex)

    def process(self):

        # Step 1 — Load embeddings
        status, emb_res = self.generate_embeddings()
        if status == "error":
            return (status, emb_res)

        # Step 2 — If transcript provided -> ingestion attempt
        if self.text and self.video_id:

            # Skip if already indexed
            if self.video_exists(emb_res):
                print("Video already exists")
                (status, res) = self.generate_vectorstore(embeddings=emb_res)
                return ("success", res)
                '''return (
                    "exists",
                    "✅ Video already indexed.",
                    Chroma(
                        persist_directory=self.vector_db_path,
                        embedding_function=emb_res
                    )
                )'''

            # Create document
            status, doc_res = self.generate_documents()
            if status == "error":
                return (status, doc_res)

            # Chunk document
            status, chunk_res = self.generate_chunks(doc_res)
            if status == "error":
                return (status, chunk_res)

            # Store vectors
            return self.generate_vectorstore(
                embeddings=emb_res,
                chunks=chunk_res
            )

        # Step 3 — Query mode (just load DB)
        return self.generate_vectorstore(embeddings=emb_res)
