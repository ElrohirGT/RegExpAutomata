import os
import time
import json
from shunYard import toPostFix
from regexpToAFN import toAFN
from AFNToAFD import fromAFNToAFD
from minimizeAFD import minimize_afd
import graphviz
from colorama import Fore, Style, init

init(autoreset=True)  # Para que los colores se reinicien automáticamente

def sanitize_folder_name(name):
    return ''.join(c if c.isalnum() else '_' for c in name)

def generate_graph(automaton, name, folder):
    dot = graphviz.Digraph(comment=name)

    if isinstance(automaton['transitions'], list):  # Para AFN (lista de transiciones)
        for state_idx, transitions in enumerate(automaton['transitions']):
            state_label = str(state_idx)
            for input_char, next_states in transitions.items():
                for next_state in next_states:
                    next_state_label = str(next_state)
                    dot.edge(state_label, next_state_label, label=input_char)
    else:  # Para AFD o AFD minimizado (diccionario de transiciones)
        for state, transitions in automaton['transitions'].items():
            state_label = ",".join(map(str, state))
            for input_char, next_state in transitions.items():
                next_state_label = ",".join(map(str, next_state))
                dot.edge(state_label, next_state_label, label=input_char)

    accepted_states = automaton['accepted'] if isinstance(automaton['accepted'], (list, set)) else [automaton['accepted']]

    for accepted_state in accepted_states:
        accepted_label = ",".join(map(str, accepted_state)) if isinstance(accepted_state, frozenset) else str(accepted_state)
        dot.node(accepted_label, shape='doublecircle')

    output_path = os.path.join(folder, f"{name}.gv")
    dot.render(output_path, format="png")
    print(f"{Fore.GREEN}Generated {name} graph at {output_path}.png")

def write_automaton_to_json(automaton, filename):
    if isinstance(automaton['transitions'], list):
        estados = list(range(len(automaton['transitions'])))
        transiciones = set()
        simbolos = set()

        for state_idx, transitions in enumerate(automaton['transitions']):
            for simbolo, next_states in transitions.items():
                simbolos.add(simbolo)
                for next_state in next_states:
                    transiciones.add((state_idx, simbolo, next_state))

        automaton_data = {
            "ESTADOS": estados,
            "SIMBOLOS": list(simbolos),
            "INICIO": [estados[0]],
            "ACEPTACION": [automaton['accepted']],
            "TRANSICIONES": [(origen, simbolo, destino) for (origen, simbolo, destino) in transiciones]
        }

    else:
        estados = list(automaton['transitions'].keys())
        transiciones = set()
        simbolos = set()

        for origen, transitions in automaton['transitions'].items():
            for simbolo, destino in transitions.items():
                simbolos.add(simbolo)
                transiciones.add((tuple(origen), simbolo, tuple(destino)))

        automaton_data = {
            "ESTADOS": [list(state) for state in estados],
            "SIMBOLOS": list(simbolos),
            "INICIO": [list(next(iter(estados)))],
            "ACEPTACION": [list(state) for state in automaton['accepted']],
            "TRANSICIONES": [(list(origen), simbolo, list(destino)) for (origen, simbolo, destino) in transiciones]
        }

    with open(filename, 'w') as file:
        json.dump(automaton_data, file, indent=4)

    print(f"{Fore.YELLOW}Automaton written to {filename}")

def simulate_regexp_process(infix_expression, test_string):
    sanitized_infix = sanitize_folder_name(infix_expression)
    folder = f"automaton_graphs/{sanitized_infix}"

    os.makedirs(folder, exist_ok=True)

    postfix = toPostFix(infix_expression)
    print(f"{Fore.CYAN}Postfix: {postfix}")

    afn = toAFN(postfix)
    print(f"{Fore.CYAN}AFN: {afn}")
    generate_graph(afn, "AFN", folder)
    write_automaton_to_json(afn, os.path.join(folder, "afn.json"))

    afd = fromAFNToAFD(afn)
    print(f"{Fore.BLUE}AFD Transitions:")
    for state, transitions in afd['transitions'].items():
        print(f"State: {Fore.YELLOW}{state} -> Transitions: {transitions}")
    print(f"{Fore.BLUE}AFD Accepted States: {afd['accepted']}")
    generate_graph(afd, "AFD", folder)
    write_automaton_to_json(afd, os.path.join(folder, "afd.json"))

    minimized_afd = minimize_afd(afd)
    print(f"{Fore.MAGENTA}Minimized AFD Transitions:")
    for state, transitions in minimized_afd['transitions'].items():
        print(f"State: {Fore.YELLOW}{state} -> Transitions: {transitions}")
    print(f"{Fore.MAGENTA}Minimized AFD Accepted States: {minimized_afd['accepted']}")
    generate_graph(minimized_afd, "Minimized_AFD", folder)
    write_automaton_to_json(minimized_afd, os.path.join(folder, "minimized_afd.json"))

    current_state = next(iter(minimized_afd['transitions'].keys()))
    print(f"{Fore.GREEN}Initial state: {current_state}")

    start_time = time.time()

    for char in test_string:
        print(f"{Fore.CYAN}Processing character: {char}")
        if char in minimized_afd['transitions'][current_state]:
            next_state = minimized_afd['transitions'][current_state][char]
            print(f"Transition from {Fore.YELLOW}{current_state} to {Fore.YELLOW}{next_state} on '{char}'")
            current_state = next_state
        else:
            print(f"{Fore.RED}No transition from {current_state} on '{char}'")
            print(f"{Fore.RED}String '{test_string}' is not accepted.")
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"{Fore.RED}Verification time: {elapsed_time} seconds")
            return False

    if current_state in minimized_afd['accepted']:
        print(f"{Fore.GREEN}String '{test_string}' is accepted.")
    else:
        print(f"{Fore.RED}Final state: {current_state} is not an accepted state.")
        print(f"{Fore.RED}String '{test_string}' is not accepted.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{Fore.YELLOW}Verification time: {elapsed_time} seconds")

if __name__ == "__main__":
    infix_expr = input("Ingrese la expresión regular en infix: ")
    test_str = input("Ingrese la cadena a probar: ")

    simulate_regexp_process(infix_expr, test_str)
