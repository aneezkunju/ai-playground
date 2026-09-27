from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Annotated, Literal


class OperationState(TypedDict, total = False) :
    a:int
    b:int
    result:int
    operation :str

def add (state:OperationState) -> OperationState :
    state["result"] = state["a"] + state["b"]
    return state

def sub(state:OperationState) -> OperationState :
    state["result"] =state["a"] - state["b"]
    return state

def check_if(state:OperationState) -> Literal["add","sub"] :
    if state["operation"] == "Add" :
        return "add"
    return "sub"

graph = StateGraph(OperationState)

graph.add_node("add_node",add)
graph.add_node("sub_node",sub)

graph.add_conditional_edges(
    START,
    check_if,
    {
        "add" :"add_node",
        "sub" : "sub_node"
    }
   
)
graph.add_edge("add_node",END)
graph.add_edge("sub_node",END)
'''
the general syntax of ocnditional edges
graph.add_conditional_edges(
    source_node,
    routing_function,
    {
        "routing_result_1": "destination_node_1",
        "routing_result_2": "destination_node_2",
    }
)
'''

compiled_state_graph = graph.compile()

if __name__ == "__main__" :
    result = compiled_state_graph.invoke(OperationState(a=10,b=5,operation ="Add"))