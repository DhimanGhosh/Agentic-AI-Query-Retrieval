from colorama import init, Fore, Style
import matplotlib.pyplot as plt
import networkx as nx


init(autoreset=True)

# Response streamer
def stream_response(chain, statement_dict):
    response_parts = []
    for chunk in chain.stream(statement_dict):
        part = chunk.content or ""
        print(Style.BRIGHT + Fore.GREEN + part, end="", flush=True)
        response_parts.append(part)
    response = "".join(response_parts).strip()
    return response

def print_response(text, end: str="", flush: bool=True):
    print(Style.BRIGHT + Fore.CYAN + text + Style.RESET_ALL, end=end, flush=flush)

def print_interrupt(text: str):
    print(Style.DIM + Fore.YELLOW + text)

def print_error(text: str):
    print(Style.BRIGHT + Fore.RED + text)

def take_input(text: str):
    return input(Style.BRIGHT + Fore.BLUE + f"{text}: ")

# Visualize the graph
def show_graph(graph):
    # Extract the LangGraph DiGraph
    langgraph_g = graph.get_graph()

    # Convert to a new networkx DiGraph
    G = nx.DiGraph()
    for edge in langgraph_g.edges:
        G.add_edge(edge.source, edge.target)

    # Visualize
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color='skyblue',
        edge_color='gray',
        node_size=3000,
        font_size=10,
        font_weight='bold'
    )
    plt.title("LangGraph Workflow")
    plt.show()
