from colorama import init, Fore, Style

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
