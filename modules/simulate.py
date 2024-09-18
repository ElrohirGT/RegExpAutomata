import os
import time
import json
from shunYard import toPostFix
from regexpToAFN import toAFN
from AFNToAFD import fromAFNToAFD
from minimizeAFD import minimize_afd

# Función para simular la aceptación de la cadena en el AFD minimizado
def simulate_afd(afd, w):
    current_state = frozenset([0])  # Estado inicial
    transitions = afd['transitions']
    acceptance_states = afd['accepted']
    path = []  # Almacena las transiciones realizadas
    
    for symbol in w:
        if symbol not in transitions[current_state]:
            return False, path  # Si el símbolo no está en las transiciones, rechazar
        path.append((current_state, symbol, transitions[current_state][symbol]))
        current_state = transitions[current_state][symbol]
    
    return current_state in acceptance_states, path

# Función para guardar autómatas en archivos .json, convirtiendo claves y valores frozenset a cadenas o listas
def save_automaton(automaton, filename):
    def frozenset_to_string(d):
        if isinstance(d, dict):
            return {str(k): frozenset_to_string(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [frozenset_to_string(i) for i in d]
        elif isinstance(d, frozenset):
            return list(d)  # Convertimos frozenset a lista
        return d

    # Convertimos el autómata, especialmente las claves y valores que son frozensets
    automaton_str_keys = frozenset_to_string(automaton)

    with open(filename, 'w') as f:
        json.dump(automaton_str_keys, f, indent=4)



# Función para crear la carpeta donde se almacenarán los archivos
def create_directory(name):
    directory = f"./{name.replace('*', 'KLEENE').replace('|', 'OR').replace('.', 'CONCAT')}"  # Evitar caracteres problemáticos
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# Función principal de simulación
def main():
    # 1. Entrada del usuario
    regexp = input("Ingresa la expresión regular: ")
    w = input("Ingresa la cadena de prueba: ")

    # 2. Convertir la expresión regular a postfix
    postfix = toPostFix(regexp)
    print(f"Expresión Postfija: {postfix}")

    # 3. Crear el AFN desde la expresión postfija
    afn = toAFN(postfix)
    print(f"AFN generado.")

    # 4. Crear el AFD a partir del AFN
    afd = fromAFNToAFD(afn)
    print(f"AFD generado.")

    # 5. Minimizar el AFD
    minimized_afd = minimize_afd(afd)
    print(f"AFD minimizado.")

    # 6. Crear la carpeta para almacenar los autómatas
    folder_name = create_directory(regexp)

    # 7. Guardar los autómatas en formato .json
    save_automaton(afn, os.path.join(folder_name, 'AFN.json'))
    save_automaton(afd, os.path.join(folder_name, 'AFD.json'))
    save_automaton(minimized_afd, os.path.join(folder_name, 'AFD_minimizado.json'))

    # 8. Simular la aceptación de la cadena en el AFD minimizado
    start_time = time.time()
    is_accepted, transitions_made = simulate_afd(minimized_afd, w)
    end_time = time.time()

    # 9. Tiempo de simulación
    simulation_time = end_time - start_time

    # 10. Mostrar el resultado de la simulación
    if is_accepted:
        print(f"La cadena '{w}' es aceptada por el autómata.")
    else:
        print(f"La cadena '{w}' NO es aceptada por el autómata.")
    
    print(f"Tiempo de simulación: {simulation_time:.6f} segundos")
    print(f"Transiciones realizadas: {transitions_made}")

    # 11. Guardar el resultado de la simulación y las transiciones en un archivo .json
    result = {
        "cadena": w,
        "resultado": "ACEPTADA" if is_accepted else "RECHAZADA",
        "tiempo": simulation_time,
        "transiciones": transitions_made
    }
    with open(os.path.join(folder_name, 'resultado.json'), 'w') as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    main()
