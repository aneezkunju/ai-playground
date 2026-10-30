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