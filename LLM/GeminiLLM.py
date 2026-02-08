from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_classic.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
import os

class GeminiLLM:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = "AIzaSyAX6n0QGoHXqrlsXtoV6zj2ejRXZp4OW6c"
    
    def generateSummary(self, chunk : str):
        try:
            model = ChatGoogleGenerativeAI(
                model="gemini-3-flash-preview",
                temperature=0.7,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
            
            # Dymanic prompt doesn't work with SystemMessage and HumanMessage
            #template = ChatPromptTemplate.from_messages([
            #    SystemMessage("You are an expert Content Summarizing Assistant"),
            #    HumanMessage("Summarize the content without considering any previous context. The #content is : {text}")
            #])

            template = ChatPromptTemplate.from_messages([
                ("system", "You are an expert Content Summarizing Assistant"),
                ("human", "Summarize the content without considering any previous context. The content is : {text}")
            ])
            
            prompt = template | model
            
            response = prompt.invoke({
                "text" : chunk
            })
            
            return ("success", response.text)
        except Exception as ex:
            print(f"Gemini error = {ex}")
            return ("error", ex)
        
        