from dotenv import load_dotenv
from claude_agent_sdk import (
    ClaudeSDKClient, 
    ClaudeAgentOptions, 
    InMemorySessionStore, 
    query, tool,
    HookCallback, HookMatcher
)
import asyncio
from utils import parse_message, MODEL_NAME
from pathlib import Path
import os



from claude_agent_sdk.types import (
    PermissionResultAllow, 
    PermissionResultDeny, 
    ToolPermissionContext
)
SCRIPT_DIR = Path(__file__).parent
DOWNLOADS_DIR = SCRIPT_DIR / "downloads"

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


async def enforce_human_only_policy(input_data,tool_use_id,context):
    tool_name = input_data.get("tool_name") if isinstance(input_data, dict) else getattr(input_data, "tool_name", None)
    tool_input = input_data.get("tool_input",{}) if isinstance(input_data, dict) else getattr(input_data, "tool_input", {})
    if tool_name in ["Read", "Edit",  "Write"]:
        file_path = tool_input.get("path") or tool_input.get("command","")
        if not is_allowed_author(file_path):
        # Return SDK denial response
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "reason": f"Access blocked: '{file_path}' was not authored by a human."
                }
            }
# Allow tool to run normally
    return {}

async def main(question:str):
    options = ClaudeAgentOptions(
            system_prompt="You are an helpful assistant",
            setting_sources=[],
            model=MODEL_NAME,
            max_turns=30,
            tools=["Read", "Glob", "Bash","WebSearch","is_allowed_author"],
            cwd=DOWNLOADS_DIR,
            permission_mode="default",
            can_use_tool=custom_tool_checker,
            hooks={
                "PreToolUse": [
                    HookMatcher(
                        matcher="*",
                        hooks =[enforce_human_only_policy])
                ]
            }
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


def is_allowed_author(path:str) ->bool :
    '''
    given a file path in the macos, the function returns if the author of the file is allowed,
    the tool will be used to determine if the basic file operations on thsi file can be done
    or not
    '''
    if not path or not isinstance(path, str):
        return True  # Fallback allow if no explicit path string was passed
    
    file_path = Path(path)
    # below is not good enough so commented opying files in macOS strips their original ownership metadata.
    # Prevent stat() calls on invalid or non-existent file paths
    # if not file_path.exists():
    #     return True
    # return file_path.stat().st_uid > 500 # allow only human authored files

    try:
        # Get list of extended attributes on macOS
        attrs = os.listxattr(file_path)
        
        # If the file has a quarantine flag, it was downloaded/externally sourced
        if "com.apple.quarantine" in attrs:
            return False  # Not locally authored / downloaded file
            
        return True  # Locally created file
    except Exception:
        return False
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(ask_question())