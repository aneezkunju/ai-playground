from langgraph.graph import StateGraph, START, END
from typing import TypedDict, NotRequired
import time

class OperationState(TypedDict):
    rate: int|float
    principal: int|float
    years: float|int
    simple_interest: NotRequired[float]
    compound_interest: NotRequired[float]


def calculate_simple_interest(state: OperationState) -> OperationState:
    state["simple_interest"] = (state["principal"] * state["rate"] * state["years"]) / 100
    return state

def calculate_compound_interest(state: OperationState) -> OperationState:
    state["compound_interest"] = state["principal"] * (1 + state["rate"] / 100) ** state["years"] - state["principal"]
    return state    


def take_inputs(keyword:str, desc:str) -> str:
    return input(f("Please enter {keyword} <{desc}> :"))



state_graph = StateGraph(OperationState)

state_graph.add_node("si",calculate_simple_interest)
state_graph.add_node("ci",calculate_compound_interest)

state_graph.add_edge(START,"si")
state_graph.add_edge("si","ci")
state_graph.add_edge("ci",END)
graph = state_graph.compile()

if "__name__" == "__main__":
    rate = float(take_inputs("rate","rate of interest"))
    principal    = float(take_inputs("principal amount" ,"How much loan do you need?"))
    years = float(take_inputs("number of years" ,"How many years will it need for you to repay?"))
    graph.invoke(OperationState (rate=rate,principal=principal,years=years))

   # operation_state:OperationState ={"rate":rate,"principal":principal,"years":years}