def toAFN(postfix: str):
    stack = []
    for char in postfix:
        match char:
            case ".":  # Concatenate
                afn2 = stack.pop()
                afn1 = stack.pop()

                afn1OriginalLength = len(afn1["transitions"])
                newAccepted = afn2["accepted"] + afn1OriginalLength

                # Add epsilon transition to start of AFN2
                afn1Accepted = afn1["accepted"]
                initializeOrAppend(
                    afn1["transitions"][afn1Accepted], "_", afn1OriginalLength
                )

                # Map AFN2 transitions to start at the end of AFN1
                mappedAFN2Transitions = displaceTransitions(afn2, afn1OriginalLength)
                afn1["transitions"] += mappedAFN2Transitions

                # Set new accepted
                afn1["accepted"] = newAccepted
                stack.append(afn1)

            case "+":  # Logical OR
                afn2 = stack.pop()
                afn1 = stack.pop()

                lenAfn1 = len(afn1["transitions"])
                afn = newAFN([{"_": [2, 2 + lenAfn1]}, {}], 1)
                afnLength = len(afn["transitions"])
                mappedAFN1Transitions = displaceTransitions(afn1, afnLength)

                afn1Accepted = afn1["accepted"]
                initializeOrAppend(mappedAFN1Transitions[afn1Accepted], "_", 1)

                afnLength += lenAfn1
                mappedAFN2Transitions = displaceTransitions(afn2, afnLength)

                afn2Accepted = afn2["accepted"]
                initializeOrAppend(mappedAFN2Transitions[afn2Accepted], "_", 1)

                mappedAFN1Transitions += mappedAFN2Transitions
                afn["transitions"] += mappedAFN1Transitions
                stack.append(afn)

            # case '*': # 0 or more
            case _:
                stack.append(newAFN([{char: [1]}, {}], 1))
    return stack.pop()


def initializeOrAppend(dictionary: dict, key: str, append):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(append)


def displaceTransitions(afn, delta: int):
    return [
        {
            word: [d + delta for d in destinations]
            for (word, destinations) in transition.items()
        }
        for transition in afn["transitions"]
    ]


def newAFN(transitions: list, accepted: int):
    return {
        "transitions": transitions,
        "accepted": accepted,
    }


# exampleAFN = {
#         'transitions': [{'_': [1,2]}, {'a':[3]}, {'b': [4]}, {'_': [5]}, {'_': [5]}, {}],
#         'accepted': 5
#         }
# print(exampleAFN)
