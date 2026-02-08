# For Generating Summaries using LangChain
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_classic.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

class LLamaLLM:
    def __init__(self):
        pass
    
    def getLLMSummary(self, chunk : str):
        try:
            model = LlamaCpp(
                model_path = "./LLMModel/Summary/TinyLlama-1.1B-Chat-v1.0-Q3_K_M.gguf",
                n_ctx = 2048,
                n_threads = 8,
                temperature = 0.3,
                verbose = False
            )
            
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage("You are an expert Content Summarizer."),
                HumanMessage(" Without hallucinating and considering any previous context, summarize the given content : {text}")
            ])
            
            llm_chain = prompt | model
            
            summary = llm_chain.invoke({
                "text" : chunk
            })
            
            print(f"Summary = \n{summary}")
            return ("success", summary)
        except Exception as ex:
            print(ex)
            return ("error", ex)