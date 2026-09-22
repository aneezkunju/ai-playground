from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import time

class OperationState(TypedDict):
    a: int
    b: int
    sum: int|None
    product: None|int
    difference: None|int


def add(state: OperationState) -> OperationState:
    state["sum"] = state["a"] + state["b"]
    return state

def multiply(state: OperationState) -> OperationState:
    state["product"] = state["a"] * state["b"]
    return state

def subtract(state: OperationState) -> OperationState:
    state["difference"] = state["a"] - state["b"]
    return state

#region commented code
# state_graph = StateGraph(
#     name="Operation Graph",
#     initial_state=OperationState(a=5, b=3, sum=None, product=None, difference=None),
#     states={
#         START: OperationState(a=5, b=3, sum=None, product=None, difference=None),
#         "add": OperationState(a=5, b=3, sum=None,               product=None, difference=None),         
#         "multiply": OperationState(a=5, b=3, sum=None,          product=None, difference=None),
#         "subtract": OperationState(a=5, b=3, sum=None,          product=None, difference=None),
#         END: OperationState(a=5, b=3, sum=None, product=None, difference=None),
#     },
#     transitions={
#         START: ["add", "multiply", "subtract"],
#         "add": ["multiply", "subtract", END],
#         "multiply": ["add", "subtract", END],
#         "subtract": ["add", "multiply", END],               

#     },
#     state_functions={
#         "add": add,
#         "multiply": multiply,           
#         "subtract": subtract,
#     },
#     transition_functions={
#         "add": lambda state: time.sleep(1) or state,
#         "multiply": lambda state: time.sleep(1) or state,               
#         "subtract": lambda state: time.sleep(1) or state,
#     }
# )   
#endregion

state_graph = StateGraph(OperationState)
state_graph.add_node("add",add)
state_graph.add_node("multiply",multiply)
state_graph.add_node("subtract",subtract)

state_graph.add_edge(START,"add")
state_graph.add_edge("add","subtract")
state_graph.add_edge("subtract","multiply")
state_graph.add_edge("multiply",END)

graph = state_graph.compile()

if __name__ == "__main__":
    result = graph.invoke(OperationState(a=5,b=4))