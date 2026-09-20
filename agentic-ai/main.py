from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain.tools   import tool
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
print (load_dotenv())

'''
Directly invoking the llm through lanchains handle for specific llms..in this case opernrouter/free
uncomment the below lins if you want to test the llm directly without using langchain chains
'''
# model = ChatOpenRouter(model="openrouter/free")
# response = model.invoke("What is the capital of France?")
# print(response.pretty_print())

@tool
def add(a: int, b: int) -> int:
    '''Adds two numbers together.'''
    return a + b

@tool
def sub(a: int, b: int) -> int:
    '''Subtracts two numbers.'''
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    '''Multiplies two numbers.'''
    return a * b   


@tool
def divide(a: int, b: int) -> float:
    '''Divides two numbers.'''
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b    


llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
agent = create_agent(llm, tools=[add, sub, multiply, divide]) 
messages = [
    SystemMessage("You are an helpful assistant"),
    HumanMessage("What is 5 + 3?"),
]


response = agent.invoke({
    "messages": [
        ("user", "What is 2 + 2?")
    ]
})

print(f"***response*******: {response}")
print(f"***type*******: {type(response)}"  )

message = response["messages"][-1]

print(f"***content*******: {message.content}")
print(f"***content_blocks*******: {message.content_blocks}")


response = agent.invoke({"messages": messages}) #invocation using the tool and the messages list
# print (response["messages"][-1].pretty_print())
# response["messages"][-1].content_b
message = response["messages"][-1]

print(f"***with tool calling content*******: {message.content}")
print(f"***with tool calling content_blocks*******: {message.content_blocks}")
