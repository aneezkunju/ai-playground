'''
commonn utilities here
'''
from typing import Callable, Any
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    create_sdk_mcp_server,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock
)

MOCK_ORDERS ={
    "customerid_123" : {
        "TB-156" : {
            "status" :"out for delivery",
            "eta" : "1500 hours",
            "items" :"3*Broast Chicken Bucket"
        }
    },
     "customerid_124" : {
            "TB-157" : {
                "status" :"Preparing",
                "eta" : "1645 hours",
                "items" :"3* Jumbo Chicken Biryani"
            }
        }
}

ENV = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY" : "1"}

def fail (text:str) ->dict[str,Any] :
    '''
    A failed tool result
    '''
    return {"Content": [{"type":"text","text":text}],
            "is_error": True}

def ok (text:str) ->dict[str,Any] :
    '''
    A success tool result
    '''
    return {"Content": [{"type":"text","text":text}]}

def get_default_options (
        system_prompt : str,
        tools : list,
        resume :str|None = None,
        max_turns : int =6
) -> ClaudeAgentOptions :
    return ClaudeAgentOptions (
        tools = [],
        allowed_tools= ["mcp__support__*"],
        max_turns= max_turns,
        resume=resume,
        system_prompt=system_prompt,
        permission_mode="dontAsk",
        env = ENV,
        mcp_servers= {"SupportAgent" :create_sdk_mcp_server(name="SupportAgent",version="1.0.0.0",tool=tools)}
    )

def print_message(message) -> None:
    if isinstance (message,AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                print(f"   [tool] {block.name.split('__')[-1]} {block.input}")
            elif isinstance(block, TextBlock):
                print(f"Agent: {block.text}")
