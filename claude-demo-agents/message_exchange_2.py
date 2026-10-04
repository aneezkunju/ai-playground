from dotenv import load_dotenv
from typing import TypedDict, Literal
from claude_agent_sdk import ClaudeAgentOptions, query
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
async def initiate_conversation (question: str |None= "What is capital of France", 
                                 tone : Literal["BASIC", "DETAILED","LIKE10"] = "BASIC") :

    
    additional_arguments = {
        "system_prompt" : TONE_DICT[tone]
    }
    options = get_default_option(**additional_arguments)
    async for message in query(prompt=question,options=options):
        parse_message(message=message)
async def ask_question():
    TONE_MAP ={
        1:"BASIC",
        2:"DETAILED",
        3:"LIKE10"
    }
    question = input("What is your question?")
    
    print("Select a tone : ")
    print("1. Basic -> Will explain you the basic ")
    print("2. Detailed -> Will explain you like a pro")
    print("3. Like10 -> Will explain you like a 10 year old")
    choice = int(input("Make your choice, by pressing the appropriate number keys"))
    tone = TONE_MAP[choice]
    if not question:
        await initiate_conversation(tone)
    else:
        await initiate_conversation(question,tone)
if __name__ == "__main__":  
    load_dotenv()
    asyncio.run(ask_question())

    