from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from prompts import (
    GRAMMAR_CORRECTOR_PROMPT, REPHRASER_PROMPT,
    RETRIEVAL_PROMPT, VALIDATOR_PROMPT
)
from pydantic import BaseModel
from typing import Optional

# Initialize the local Ollama model
llm = ChatOllama(
    model="mistral:latest",
    temperature=0.2
)

# Response streamer
def stream_response(chain, statement_dict):
    response_parts = []
    for chunk in chain.stream(statement_dict):
        part = chunk.content or ""
        print(part, end="", flush=True)
        response_parts.append(part)
    response = "".join(response_parts).strip()
    return response

# Agent 0: Grammar Corrector
def grammar_corrector_agent(state):
    statement = state.statement
    prompt = ChatPromptTemplate.from_messages([
        ("system", GRAMMAR_CORRECTOR_PROMPT),
        ("human", "{statement}")
    ])
    chain = prompt | llm
    print("\nGrammar Corrector Agent: Corrected statement:\n", end="", flush=True)

    # Streaming response
    corrected_statement = stream_response(chain, {"statement": statement})

    return {"statement": corrected_statement}

# Agent 1: Rephraser
def rephraser_agent(state):
    statement = state.statement
    prompt = ChatPromptTemplate.from_messages([
        ("system", REPHRASER_PROMPT),
        ("human", "{statement}")
    ])
    chain = prompt | llm
    print("\nRephraser Agent: Rephrased statement:\n", end="", flush=True)

    # Streaming response
    rephrased = stream_response(chain, {"statement": statement})

    return {"rephrased_statement": rephrased}

# Agent 2: Retriever
def retriever_agent(state):
    rephrased_statement = state.rephrased_statement
    prompt = ChatPromptTemplate.from_messages([
        ("system", RETRIEVAL_PROMPT),
        ("human", "{rephrased_statement}")
    ])
    chain = prompt | llm
    print("\n\nRetriever Agent: Retrieved answer:\n", end="", flush=True)

    # Streaming response
    retrieved_answer = stream_response(chain, {"rephrased_statement": rephrased_statement})

    return {"retrieved_answer": retrieved_answer}

# Agent 3: Validator
def validator_agent(state):
    retrieved_answer = state.retrieved_answer
    prompt = ChatPromptTemplate.from_messages([
        ("system", VALIDATOR_PROMPT),
        ("human", "{retrieved_answer}")
    ])
    chain = prompt | llm
    print("\n\nSummarizing:\n", end="", flush=True)

    # Streaming response
    best_response = stream_response(chain, {"retrieved_answer": retrieved_answer})

    return {"final_answer": best_response}

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

# Execution function
def run_agentic_system(statement: str):
    initial_state = {"statement": statement}
    result = graph.invoke(initial_state)
    return result["final_answer"]

# Run the agentic system
if __name__ == '__main__':
    input_statement = input("Enter a statement: ")
    run_agentic_system(input_statement)
