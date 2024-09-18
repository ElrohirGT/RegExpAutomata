# minimizeAFD.py

def minimize_afd(afd):
    grouped = {}
    
    # Agrupar los estados del AFD con las mismas transiciones
    for state, transitions in afd['transitions'].items():
        key = frozenset(transitions.items())  # Usar las transiciones como clave
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

        if any(state in afd['accepted'] for state in group):
            minimized_accepted.add(representative)

    return {
        'transitions': minimized_transitions,
        'accepted': list(minimized_accepted)
    }
