from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_classic.prompts import ChatPromptTemplate, PromptTemplate
#from langchain_classic.globals import set_debug
import langchain_classic.globals
from langchain_classic.cache import InMemoryCache
from langchain_core.output_parsers import StrOutputParser
import os

class FalconsLLM:
    def __init__(self):
        langchain_classic.globals.set_debug(False)
        langchain_classic.globals.set_llm_cache(InMemoryCache())
        #self.llm_pipeline = pipeline("text-generation", model="Falconsai/text_summarization", device=0)
        self.llm_pipeline = pipeline("summarization", model="Falconsai/text_summarization")
    
    def generateSummary(self, chunk : str):
        try:
            '''
            model = HuggingFacePipeline(pipeline=self.llm_pipeline, verbose=False)
            
            #prompt = ChatPromptTemplate([
            #    ("system", "You are an expert Content Summarizing Assistant"),
            #    ("human", "Summarize the content without considering any previous context. The content #is : {text}")
            #])
            
            prompt = PromptTemplate.from_template("summarize: {text}")
            
            chain = prompt | model | StrOutputParser()
            
            response = chain.invoke({
                "text" : chunk
            })
            
            return ("success", response)'''
            prompt = PromptTemplate.from_template("{text}")
            print(f"Prompt = {prompt}")
            #response = self.llm_pipeline(prompt)
            response = self.llm_pipeline(chunk, do_sample=False)
            print(f"Response = {response}")
            
            return ("success", response)
        except Exception as ex:
            print(ex)
            return ("error", ex)