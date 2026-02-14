from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

class RAGService:
    def __init__(self, vector_stores : Chroma):
        load_dotenv()
        self.vectore_stores = vector_stores
        self.retriever = self.vectore_stores.as_retriever(
            search_type="similarity",
            search_kwargs = {"k" : 4}
        )
        
    def generator(self, question : str):
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.3
            )
            
            prompt = ChatPromptTemplate.from_template("""
                    You are answering questions about a YouTube video.

                    Use ONLY the provided context to answer.
                    If the answer is not in the context, say:
                    "I could not find this in the video."

                    Context:
                    {context}

                    Question:
                    {question}
                    """)
            
            rag_chain = (
                {
                    "context" : self.retriever | self.format_docs,
                    "question" : RunnablePassthrough()
                }
                | prompt | llm | StrOutputParser()
            )
            
            response = rag_chain.invoke(question)
            
            print(f"Answer = {response}")
            
            return ("success", response)
        except Exception as ex:
            print(f"{ex}")
            return ("error", ex)
    
    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
    #