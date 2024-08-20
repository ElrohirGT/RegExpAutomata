from regexpToAFN import toAFN
from pprint import pp

type AFDState = frozenset[int]
type AFDTransitions = dict[AFDState, dict[str, AFDState]]


def fromAFNToAFD(afn):
    afdTransitions: AFDTransitions = {}
    closure, inputs = findClosure(afn, 0, set(()))
    travelAFN(afn, frozenset(closure), frozenset(inputs), afdTransitions)

    accepted = []
    for state in afdTransitions:
        if afn["accepted"] in state:
            accepted.append(state)

    return newAFD(afdTransitions, accepted)


def travelAFN(
    afn: dict,
    closure: frozenset,
    inputs: frozenset,
    stateTransitions: AFDTransitions,
):
    if closure in stateTransitions:
        return

    stateTransitions[closure] = {}

    for i in inputs:
        if i == "_":
            continue
        reach = set(())
        reachInputs = set(())
        for stateIdx in closure:
            state = afn["transitions"][stateIdx]
            if i not in state:
                continue
            for targetIdx in state[i]:
                target, targetInput = findClosure(afn, targetIdx, set(()))
                reach |= target
                reachInputs |= targetInput

        reach = frozenset(reach)
        stateTransitions[closure][i] = reach
        travelAFN(afn, reach, frozenset(reachInputs), stateTransitions)


def findClosure(afn: dict, stateIdx: int, alreadyEvaluated: set) -> tuple[set, set]:
    """
    Finds the closure of a given state in the provided AFN.

    Returns all the states within the closure and the set of valid inputs for the closure.
    """

    if stateIdx in alreadyEvaluated:
        return ([], set(()))

    alreadyEvaluated.add(stateIdx)

    original = afn["transitions"][stateIdx]
    closure = set([stateIdx])
    inputs = set(original.keys())

    if "_" in original:
        for state in original["_"]:
            foundClosure, foundInputs = findClosure(afn, state, alreadyEvaluated)
            closure |= foundClosure
            inputs |= foundInputs

    return (closure, inputs)


def initializeOrAppend():
    pass


def newAFD(transitions: AFDTransitions, accepted: list[AFDState]):
    """
    Constructs a new AFD given the transistions and it's accepted states.
    """
    return {"transitions": transitions, "accepted": accepted}


if __name__ == "__main__":
    postfix = "a*"
    print("RegExp:", postfix)

    afn = toAFN(postfix)
    print("AFN ")
    pp(afn)

    afd = fromAFNToAFD(afn)
    print("AFD")
    pp(afd)
