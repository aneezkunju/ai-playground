from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, InMemorySessionStore, query
import asyncio
from utils import parse_message, MODEL_NAME
from pathlib import Path
import sys, platform
import csv


from claude_agent_sdk.types import (
    PermissionResultAllow, 
    PermissionResultDeny, 
    ToolPermissionContext
)


# CSV_PATH =Path("install-softwares-experiment/install_softwares.csv")
CSV_PATH =Path("install_softwares.csv")

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

async def process_each_install_swoftware_record(name:str, target_version:str, download_url:str) :
    current_os= platform.system().lower()
    if current_os == "windows":
        terminal_guidlines ="""
        Target OS : Windows
        - Use Powershell or windows cli utilities
        - using where.exe  <name of software> or Get-Command <name of software> findif the software is installed
        - Download the software using PowerShell Invoke-WebRequest or curl.exe
        - move the binaries to C:\\Windows\\System32 or any dir in PATH
        """
    else :
        terminal_guidlines = f"""
        Target OS : {current_os}
        - Use command -v <name of software> or which <name of software>
        - Download the software using curl or wget
        - move binaries to 'usr/local/bin' and run 'chmod +x'
        """
    system_prommpt = f"""
        you are an helpful system administrator, with full authority to install softwares 
        {terminal_guidlines}
        FOR {name}:
        1. Check if {name} is instaslled and retreive its current version
        2. If Target Version is 'Latest': Check for the newest release asset from '{download_url}', compare with installed version, and install/upgrade if outdated or missing.
        3. If Target Version is explicit (e.g. '15.2.0'): Compare installed version with '{target_version}'. If installed version < '{target_version}' or missing, download and install/upgrade.
        4. If already installed and up to date: Output that '{name}' is already up to date and DO NOT download.
    """
    options = ClaudeAgentOptions(
                system_prompt= system_prommpt,
                setting_sources=[],
                model=MODEL_NAME,
                max_turns=30,
                tools=["Read", "Glob", "Bash","WebSearch"],
                permission_mode="default",
                can_use_tool=custom_tool_checker
            )
    prompt = f"Check and manage software '{name}' (Target Version: {target_version}) from link: {download_url}"
    async with ClaudeSDKClient(options=options) as client:
            # question = input("Give any instruction about downloads folder")
            await client.query(prompt)
            '''
            Inside main, receive_messages() keeps reading until the client’s message stream closes. But that stream is only closed when the async
            with client context exits, and that context can’t exit until the loop finishes. Use receive_response() instead: it stops when Claude 
            sends a ResultMessage, letting main() return and the outer loop continue.
            '''
            # async for message in client.receive_messages(): this never returns
            async for message in client.receive_response():
                parse_message(message)


    
    

async def run_csv():
    with open(CSV_PATH, mode = "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            name = row["name"]
            version = row["version"]
            url_to_download = row["url_to_download"]
            await process_each_install_swoftware_record(name,version,url_to_download)
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(run_csv())