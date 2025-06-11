from agent.graph_builder import graph
from utils import print_interrupt, print_error, take_input, show_graph


# Execution function
def run_agentic_system(statement: str):
    initial_state = {"statement": statement}
    result = graph.invoke(initial_state)
    return result["final_answer"]

# Run the agentic system
if __name__ == '__main__':
    try:
        input_statement = take_input("Enter a statement")
        run_agentic_system(input_statement)
        viz_graph = take_input("\n\nVisualize the graph? (y/n)")
        if viz_graph.lower() == "y":
            show_graph(graph)
    except KeyboardInterrupt:
        print_interrupt("\n\nProgram interrupted by user.")
    except Exception as e:
        print_error(f"\n\nAn error occurred: {e}")
