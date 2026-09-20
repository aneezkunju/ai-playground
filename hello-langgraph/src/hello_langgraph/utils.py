from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

load_dotenv()

def get_default_chat_model() -> BaseChatModel:  
    '''
    Returns default google free model
    '''
    model_name ="google_genai:gemini-3.5-flash-lite"
    model = init_chat_model(model=model_name)
    return model