from agent.agents import (
    grammar_corrector_agent, rephraser_agent,
    retriever_agent, validator_agent
)
from typing import Optional
from langgraph.graph import StateGraph, END
from pydantic import BaseModel


# Define the state schema
class AgentState(BaseModel):
    statement: str
    rephrased_statement: Optional[str] = None
    retrieved_answer: Optional[str] = None
    final_answer: Optional[str] = None

# Create the langgraph state graph
graph_builder = StateGraph(state_schema=AgentState)

# Add agents as nodes
graph_builder.add_node("grammar_corrector", grammar_corrector_agent)
graph_builder.add_node("rephraser", rephraser_agent)
graph_builder.add_node("retriever", retriever_agent)
graph_builder.add_node("validator", validator_agent)

# Add edges for flow
graph_builder.set_entry_point("grammar_corrector")
graph_builder.add_edge("grammar_corrector", "rephraser")
graph_builder.add_edge("rephraser", "retriever")
graph_builder.add_edge("retriever", "validator")
graph_builder.add_edge("validator", END)

# Compile the graph
graph = graph_builder.compile()
