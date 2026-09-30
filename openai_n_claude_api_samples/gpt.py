from openai import OpenAI
from dotenv import load_dotenv
import os

def interact_with_model():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(max_output_tokens=100,
                                       model="gpt-5.6-luna",
                                       input="What is capital of France?")
    
    print(f" The response from gpt: {response.output_text}")

    print (f"The input tokens used :{response.usage.input_tokens}")
    print (f"The output tokens used {response.usage.output_tokens}")
    print(f"Input token details {response.usage.input_tokens_details}")
    print(f"Output token details {response.usage.output_tokens_details}")
    
if __name__=="__main__":
    interact_with_model()