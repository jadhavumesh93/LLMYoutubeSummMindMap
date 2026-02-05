from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

class LLMService:
    def __init__(self):
        self.PUNCT_MODEL = "oliverguhr/fullstop-punctuation-multilang-large"
    
    