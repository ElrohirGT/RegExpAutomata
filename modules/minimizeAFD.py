# minimizeAFD.py

def minimize_afd(afd):
    grouped = {}
    for state, transitions in afd['transitions'].items():
        key = frozenset(transitions.keys())
        grouped.setdefault(key, []).append(state)

    minimized_transitions = {}
    minimized_accepted = set()

    for group in grouped.values():
        representative = group[0]
        new_state = frozenset(group)
        minimized_transitions[new_state] = {}

        for input_char, next_state in afd['transitions'][representative].items():
            for next_group in grouped.values():
                if next_state in next_group:
                    minimized_transitions[new_state][input_char] = frozenset(next_group)
                    break

        if any(state in afd['accepted'] for state in group):
            minimized_accepted.add(new_state)

    return {
        'transitions': minimized_transitions,
        'accepted': list(minimized_accepted)
    }
