from dotenv import load_dotenv
from typing import TypedDict, Literal
from claude_agent_sdk import ClaudeAgentOptions, query, ClaudeSDKClient, ResultMessage
from utils import get_default_option, parse_message
import os, asyncio


TONE_DICT = {
    'DETAILED': """You are a tutor, Explain the question asked in a 
    direct fashion. Ensure you add some examples to answer the question""",
    'BASIC': """ You are a tutor, The question asked is before an exam, 
    Help in quickly revising to recollect the learnt topic and give simple, 
    crisp and necessary stuff.
    """,
    'LIKE10': """You are a tutor, The question asked by the student who has
    zero or minimal conceptual knowledge. Dont make assumptions, Answer the question
    in a elaborate fashion right from concepts required to answer the question.
    """
}

name_session_dict ={}
async def initiate_conversation (name: str,
                                 question: str |None= "What is capital of France", 
                                 tone : Literal["BASIC", "DETAILED","LIKE10"] = "BASIC",
                                 ) :

    
    additional_arguments = {
        "system_prompt" : TONE_DICT[tone],
        "setting_sources": [],
    }
    session_id = name_session_dict.get(name)
    if session_id:
        additional_arguments["resume"] = session_id
    options = get_default_option(**additional_arguments)
    
    # async for message in query(prompt=question,options=options):
    #     parse_message(message=message)
    async with ClaudeSDKClient(options=options) as client:
        await client.query(question)
        async for message in client.receive_response():
            parse_message(message=message)
            if isinstance(message,ResultMessage) and message.session_id : 
                name_session_dict[name] = message.session_id


async def ask_question():
    TONE_MAP ={
        1:"BASIC",
        2:"DETAILED",
        3:"LIKE10"
    }
    while True:
        name = input("What is your name?")
        question = input("What is your question?")
        print("Select a tone : ")
        print("1. Basic -> Will explain you the basic ")
        print("2. Detailed -> Will explain you like a pro")
        print("3. Like10 -> Will explain you like a 10 year old")
        choice = int(input("Make your choice, by pressing the appropriate number keys"))
        tone = TONE_MAP[choice]
        if question:
            await initiate_conversation(name, question, tone)
        else:
            await initiate_conversation(name, tone=tone)

        if input("Press Z to exit, or Enter to ask another question: ").strip().upper() == "Z":
            break
if __name__ == "__main__":  
    load_dotenv()
    asyncio.run(ask_question())

    