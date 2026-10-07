from dotenv import load_dotenv
from  claude_agent_sdk import (
    ClaudeAgentOptions,
    Message,
    SystemMessage,
    ResultMessage,
    AssistantMessage,
    TextBlock,
    UserMessage
)

import os

MODEL_NAME ="claude-haiku-4-5"

def get_default_option(**arguments) -> ClaudeAgentOptions:    
   
    settings= {
        "model": MODEL_NAME,
        "max_turns":  3,
    }
    settings.update(arguments)
    options = ClaudeAgentOptions (**settings )
    return options

def parse_message(message: Message): 
    if isinstance(message, SystemMessage):
        print(f"*******SYSTEM MESSAGE STARTS ******")
        print(f"subtype: {message.subtype}")
        print(f"*******SYSTEM MESSAGE ENDS ******")

    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block,TextBlock):
                print(f"*******ASISSTANT MESSAGE STARTS ******")
                print(block.text)
                print(f"*******ASISSTANT MESSAGE ENDS ******")

    elif isinstance(message, ResultMessage):
        print(f"*******RESULT MESSAGE STARTS ******")
        print(f"duration: {message.duration_ms} ms")
        print(f"cost in usd: {message.total_cost_usd} ms")
        if message.session_id :
            print(f"\033[1mNOTE THE SESSION ID: {message.session_id}\033[m]")
        print(f"*******RESULT MESSAGE ENDS ******")