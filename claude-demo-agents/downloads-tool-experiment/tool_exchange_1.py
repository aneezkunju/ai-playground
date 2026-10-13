from dotenv import load_dotenv
from utils import get_default_option,parse_message,MODEL_NAME
import os
from claude_agent_sdk import ClaudeSDKClient,InMemorySessionStore,query,ClaudeAgentOptions
import asyncio
from pathlib import Path

DOWNLOADS_DIR = Path("downloads-tool-experiment/downloads")

async def main() :
    options = ClaudeAgentOptions (
        setting_sources=[],
        model=MODEL_NAME,
        system_prompt="You are an helpful assistant",
        max_turns=30,
        tools = ["Read","Bash","Glob"],
        cwd=DOWNLOADS_DIR,
        permission_mode= "bypassPermissions"
    )
    async with ClaudeSDKClient(options=options) as client:
        question = input("Give me any instructions with regards to this fake download folder")
        await client.query(question)
        async for message in client.receive_messages():
            parse_message(message)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())