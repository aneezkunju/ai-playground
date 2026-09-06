import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import AIMessage, SystemMessage, HumanMessage

    #print(load_dotenv())
load_dotenv()
llm = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")
    # result = llm.invoke ("What is capital of France?")
    #  print (result)
print("main")
agent = create_agent("google_genai:gemini-3.1-flash-lite")

response = agent.invoke("what is capital of france?")
print (response)


@tool
def add(a,b):
    '''Add two numbers together
    Args:
    a the first number
    b the second number'''
    return a+b
@tool
def sub(a,b):
    '''Subtracts two numbers
    Args:
    a the first number
    b the second number'''
    return a-b
@tool
def mul(a,b):
    '''Multiplies two numbers
    Args:
    a the first number
    b the second number'''
    return a*b
@tool
def div (a,b):
    '''Divides two numbers and returns the quotient of the division ooperation
    Args:
    a the numerator
    b the denominator
    the return value is the quotient of the division operation'''
    if b == 0:
        raise Exception("b cannot be zero")
    return a/b

@tool
def mod (a,b) :
    '''Divides the two numbers and returns the remainder of the division operation
    Args:
    a the numerator
    b the denominator
    return value is the remainder of the division operation'''
    if (b==0):
     raise Exception("b cannot be zero")
    return a%b


    '''if __name__ == "__main__":
        agent.main()'''