from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, InMemorySessionStore, query
import asyncio
from utils import parse_message, MODEL_NAME
from pathlib import Path



from claude_agent_sdk.types import (
    PermissionResultAllow, 
    PermissionResultDeny, 
    ToolPermissionContext
)

DOWNLOADS_DIR = Path("downloads-tool-experiment/downloads")

# 1. Define the callback function
async def custom_tool_checker(
    tool_name: str, 
    input_data: dict, 
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    
    print(f"\nTool Requested: {tool_name}")
    print(f"Inputs: {input_data}")
    
    # Simple console approval check
    user_response = input("Allow Claude to run this tool? (y/n): ")
    
    if user_response.lower() == 'y':
        return PermissionResultAllow(behavior='allow')
    else:
        return PermissionResultDeny(behavior='deny', reason="User rejected the tool execution.")



async def main(question:str):
    options = ClaudeAgentOptions(
            system_prompt="You are an helpful assistant",
            setting_sources=[],
            model=MODEL_NAME,
            max_turns=30,
            tools=["Read", "Glob", "Bash","WebSearch"],
            cwd=DOWNLOADS_DIR,
            permission_mode="default",
            can_use_tool=custom_tool_checker
        )
    async with ClaudeSDKClient(options=options) as client:
        # question = input("Give any instruction about downloads folder")
        await client.query(question)
        '''
        Inside main, receive_messages() keeps reading until the client’s message stream closes. But that stream is only closed when the async
        with client context exits, and that context can’t exit until the loop finishes. Use receive_response() instead: it stops when Claude 
        sends a ResultMessage, letting main() return and the outer loop continue.
        '''
        # async for message in client.receive_messages(): this never returns
        async for message in client.receive_response():
            parse_message(message)

async def ask_question():
    while True:
            question = input("Give any instruction about downloads folder")
            await main(question = question)
            if input("Press Z to exit, or Enter to ask another question: ").strip().upper() == "Z":
                break
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(ask_question())