
def toAFN(postfix: str):
    stack = []
    for char in postfix:
        match char:
            case '.': # Concatenate
                afn2 = stack.pop()
                afn1 = stack.pop()

                afn1OriginalLength = len(afn1['transitions'])
                newAccepted = afn2['accepted'] + afn1OriginalLength

                # Add epsilon transition to start of AFN2
                afn1Accepted = afn1['accepted']
                if '_' not in afn1['transitions'][afn1Accepted]:
                    afn1['transitions'][afn1Accepted]['_'] = []
                afn1['transitions'][afn1Accepted]['_'].append(afn1OriginalLength)

                # Map AFN2 transitions to start at the end of AFN1
                mappedAfn2Transitions = [{word:[d+afn1OriginalLength for d in destinations] for (word,destinations) in transition.items()} for transition in afn2['transitions']]
                afn1['transitions'] += mappedAfn2Transitions

                # Set new accepted
                afn1['accepted'] = newAccepted
                stack.append(afn1)

            # case '*': # 0 or more
            # case '+': # Logical OR
            case _:
                stack.append(newAFN([{char: [1]}, {}], 1))
    return stack.pop()

def newAFN(transitions: list, accepted: int):
    return {
            'transitions': transitions,
            'accepted': accepted,
            }

# exampleAFN = {
#         'transitions': [{'_': [1,2]}, {'a':[3]}, {'b': [4]}, {'_': [5]}, {'_': [5]}, {}],
#         'accepted': 5
#         }
# print(exampleAFN)
