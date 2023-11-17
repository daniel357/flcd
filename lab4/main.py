from finite_automata import parse_automaton_data


def display_menu():
    print("----------------")
    print("0. Quit")
    print("1. States")
    print("2. Alphabet")
    print("3. Transitions")
    print("4. Initial State")
    print("5. Final States")
    print("6. Check Sequence")
    print("-----------------")


def show_states(states):
    print("Set of States: ")
    for state in states:
        print(state, end=" ")
    print()


def show_alphabet(alphabets):
    print("FA Alphabet: ")
    for alpha in alphabets:
        print(alpha, end=" ")
    print()


def show_final_states(final_states):
    print("Set of Final States: ")
    for state in final_states:
        print(state, end=" ")
    print()


def show_transitions(transitions):
    print("Set of Transitions: ")
    for key in transitions.keys():
        print("({}, {}) => {}".format(key[0], key[1], transitions[key]))


if __name__ == '__main__':
    finiteAutomata = parse_automaton_data("FA.in")
    done = False

    while not done:
        display_menu()
        print("Your choice >>>")
        choice = int(input())
        if choice == 0:
            done = True
            print("Goodbye")
        elif choice == 1:
            show_states(finiteAutomata.states)
        elif choice == 2:
            show_alphabet(finiteAutomata.alphabet)
        elif choice == 3:
            show_transitions(finiteAutomata.transitions)
        elif choice == 4:
            print("Initial State: {}".format(finiteAutomata.initial_state))
        elif choice == 5:
            show_final_states(finiteAutomata.final_states)
        elif choice == 6:
            print("Enter Sequence: ")
            sequence = input()
            if finiteAutomata.is_sequence_accepted(sequence):
                print("Sequence accepted")
            else:
                print("Sequence not accepted")
        else:
            print("Invalid option")
