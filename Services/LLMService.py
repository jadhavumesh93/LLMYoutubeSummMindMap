# For project path resolution
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from YoutubeUtility.Utility import YoutubeUtility
# For Punctuating Sentences using Transformer
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
# Summarization using Actual LLMs
#from LLM.LLamaLLM import LLamaLLM
#from LLM.GeminiLLM import GeminiLLM
from LLM.FalconsLLM import FalconsLLM

class LLMService:
    def __init__(self):
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
        self.PUNCT_MODEL = "oliverguhr/fullstop-punctuation-multilang-large"
        # Get project root directory
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Define model directory inside project root
        self.MODEL_DIR = os.path.join(PROJECT_ROOT, "LLMModel")

        # Create directory if it doesn't exist
        os.makedirs(self.MODEL_DIR, exist_ok=True)
        self.punctuator = AutoTokenizer.from_pretrained(self.PUNCT_MODEL, cache_dir=self.MODEL_DIR)
        self.punctuator_model = AutoModelForTokenClassification.from_pretrained(self.PUNCT_MODEL, cache_dir=self.MODEL_DIR)
        
        self.youtube_utility = YoutubeUtility()
        
        # Config for Sliding window sentence chunking
        self.window = 1
        
    def generateSentencePunct(self, raw_text : str = None):
        try:
            #punctuator = AutoTokenizer.from_pretrained(self.PUNCT_MODEL)
            #punctuator_model = AutoModelForTokenClassification.from_pretrained(self.PUNCT_MODEL)
            #punctuator_model.eval()
            self.punctuator_model.eval()
            inputs = self.punctuator(raw_text, return_tensors="pt", truncation=True)
            with torch.no_grad():
                outputs = self.punctuator_model(**inputs)
                
            predictions = torch.argmax(outputs.logits, dim=-1)[0]
            tokens = self.punctuator.convert_ids_to_tokens(inputs["input_ids"][0])
            labels = [self.punctuator_model.config.id2label[p.item()] for p in predictions]
            
            result = list()
            current_word = ""
            
            for token, label in zip(tokens, labels):
                # Skip special tokens
                if token in ["<s>", "</s>", "<pad>"]:
                    continue

                if token.startswith("▁"):
                    # Start new word
                    if current_word:
                        result.append(current_word)
                    current_word = token[1:]
                else:
                    # Continue current word
                    current_word += token

                # Append punctuation if predicted
                if label != "0":
                    current_word += label[-1]  # .,?! etc.   
                
            # Append last word
            if current_word:
                result.append(current_word)
            punctuated_text = " ".join(result)
            print(f"Punctuated text = \n{punctuated_text}")
            return ("success", punctuated_text)
        except Exception as ex:
            print(f"Exception = {ex}")
            return ("error", self.youtube_utility.error_codes("ERR_5"))
        
    def generateSummary(self, punctuated_text : str = None):
        try:
            start, end = 0, -1
            sentence_list = punctuated_text.split(".")
            chunk_summary = list()
            while((end < len(sentence_list)) or (end != -1)):
                sent_chunk = sentence_list[start : end]
                chunk = ".".join(sent_chunk)
                
                (status, res) = self.getLLMSummary(chunk)
                if(status == "error"):
                    #raise Exception("LLM Service problem")
                    return ("error", res)
                chunk_summary.append(res)
                
                # Set the start and end for the next set of sentence chunk
                #start += self.window
                #end += self.window
                
                # Reset condition
                if(end >= len(sentence_list)):
                    end = len(sentence_list)
            
            # Get Summary for the List of Chunk Summaries from LLM
            print(f"Chunk Combined summary = \n{''.join(chunk_summary)}")
            (status, res) = self.getLLMSummary("".join(chunk_summary))
            
            print(f"Final Summary = \n{res}")
            
            return (status, res)
        except Exception as ex:
            print(ex)
            return ("error", ex)
    
    def getLLMSummary(self, text : str):
        try:
            # Send the chunk to LLM for summarization
            (status, res) = ("error", "test error") # Default case
            # 1. LLamaLLM
            #llama_llm = LLamaLLM()
            #(status, res) = llama_llm.getLLMSummary(chunk)
            # 2. Gemini LLM
            #gemini_llm = GeminiLLM()
            #(status, res) = gemini_llm.generateSummary(chunk)
            # 3. FalconsAI
            falcons_llm = FalconsLLM()
            (status, res) = falcons_llm.generateSummary(text)
            return (status, res)
        except Exception as ex:
            print(f"{ex}")
            return ("error", ex)
    
    def process(self, raw_text : str = None):
        # 1. Check if Raw Transcript is provided
        if(raw_text == None):
            return ("error", self.youtube_utility.error_codes("ERR_6"))
        
        # 2. Check if LLM performs Punctuation
        (status, res) = self.generateSentencePunct(raw_text)
        if(status == "error"):
            return (status, res)
    
        # 3. Chunk the entire LLM Punctuated Text into list of sentences
        (status, res) = self.generateSummary(res)
        return (status, res)