# minimizeAFD.py

def minimize_afd(afd):
    # Separar los estados de aceptación y los no aceptados
    accepted_states = set(afd['accepted'])
    non_accepted_states = set(afd['transitions'].keys()) - accepted_states

    grouped = {}
    
    # Agrupar los estados del AFD con las mismas transiciones
    for state, transitions in afd['transitions'].items():
        # Crear la clave en función de las transiciones y si el estado es de aceptación o no
        is_accepted = state in accepted_states
        key = (frozenset(transitions.items()), is_accepted)  # Transiciones y si es estado aceptado

        grouped.setdefault(key, []).append(state)

    minimized_transitions = {}
    minimized_accepted = set()

    # Reasignar los estados minimizados
    for group in grouped.values():
        representative = frozenset().union(*group)  # Aplanar los estados agrupados
        minimized_transitions[representative] = {}

        for input_char, next_state in afd['transitions'][group[0]].items():
            # Encontrar a qué grupo pertenece el siguiente estado
            for next_group in grouped.values():
                if next_state in next_group:
                    next_representative = frozenset().union(*next_group)  # Aplanar también
                    minimized_transitions[representative][input_char] = next_representative
                    break

        # Si alguno de los estados del grupo es aceptado, todo el grupo es aceptado
        if any(state in accepted_states for state in group):
            minimized_accepted.add(representative)

    return {
        'transitions': minimized_transitions,
        'accepted': list(minimized_accepted)
    }
