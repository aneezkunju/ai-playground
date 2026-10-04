from dotenv import load_dotenv
import os
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio
from utils import get_default_option, parse_message
async def initiate_conve():
    
    question ="Tell nme the difference between function and generator"
    
    options = get_default_option()
    '''
    WHY IS ASYNC NEEDED BELOW:
    Because the Claude SDK is streaming the answer as it arrives, 
    not returning one finished result all at once.
    '''
    async for message in query(prompt=question,options=options):
        parse_message (message)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(initiate_conve())