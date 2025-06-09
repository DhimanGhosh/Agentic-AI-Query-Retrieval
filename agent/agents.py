from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from agent.prompts import (
    GRAMMAR_CORRECTOR_PROMPT, REPHRASER_PROMPT,
    RETRIEVAL_PROMPT, VALIDATOR_PROMPT
)
from configparser import ConfigParser
from utils import stream_response, print_response

# Load config file
config = ConfigParser()
config.read('config.ini')

# Initialize the local Ollama model
llm = ChatOllama(
    model=config['Ollama']['model'],
    temperature=float(config['Ollama']['temperature'])
)

# Agent 0: Grammar Corrector
def grammar_corrector_agent(state):
    statement = state.statement
    prompt = ChatPromptTemplate.from_messages([
        ("system", GRAMMAR_CORRECTOR_PROMPT),
        ("human", "{statement}")
    ])
    chain = prompt | llm
    print_response("\nGrammar Corrector Agent: Corrected statement:\n", end="", flush=True)

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
    print_response("\nRephraser Agent: Rephrased statement:\n", end="", flush=True)

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
    print_response("\n\nRetriever Agent: Retrieved answer:\n", end="", flush=True)

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
    print_response("\n\nSummarizing:\n", end="", flush=True)

    # Streaming response
    best_response = stream_response(chain, {"retrieved_answer": retrieved_answer})

    return {"final_answer": best_response}
