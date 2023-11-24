def parse_automaton_data(file_name="FA.txt"):
    # Open and read the file
    with open(file_name) as file:
        # Extracting states, alphabet, initial state, and final states
        state_info = file.readline().strip().split(' ')[2:]
        states = state_info
        alphabet_info = file.readline().strip().split(' ')[2:]
        alphabet = alphabet_info
        initial_state_info = file.readline().strip().split(' ')[2]
        initial_state = initial_state_info
        final_state_info = file.readline().strip().split(' ')[2:]
        final_states = final_state_info

        file.readline()  # Skip a line

        transitions = {}
        # Parsing transition data
        for line in file:
            clean_line = line.strip().replace('(', '').replace(')', '').replace(',', '').replace('=>', ' ').split(' ')
            source_state = clean_line[0]
            value = clean_line[1]
            destination_state = clean_line[2]
            # Storing transitions in a dictionary
            for letter in value:
                if (source_state, letter) in transitions.keys():
                    transitions[(source_state, letter)].append(destination_state)
                else:
                    transitions[(source_state, letter)] = [destination_state]

        # Validating states, initial state, final states, and transitions
        validate_states(states, initial_state, final_states, transitions, alphabet)
        # Creating an instance of Automaton
        return FiniteAutomata(states, alphabet, initial_state, final_states, transitions)


class FiniteAutomata:
    def __init__(self, states, alphabet, initial_state, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    def is_deterministic(self):
        # Checking if the automaton is deterministic
        for key in self.transitions.keys():
            transition_count = len(self.transitions[key])
            if transition_count > 1:
                return False
        return True

    def is_sequence_accepted(self, sequence):
        if not self.is_deterministic():
            return False
        else:
            current_state = self.initial_state
            for value in sequence:
                # Checking for valid transitions
                if (current_state, value) in self.transitions.keys():
                    current_state = self.transitions[(current_state, value)][0]
                else:
                    return False, None
            return current_state in self.final_states, current_state


def validate_states(states, initial_state, final_states, transitions, alphabet):
    # Validating states, initial state, final states, and transitions
    if initial_state not in states:
        raise Exception("Invalid initial state.")
    for final_state in final_states:
        if final_state not in states:
            raise Exception("Invalid final state.")
    for key in transitions.keys():
        src = key[0]
        if src not in states:
            raise Exception("Invalid transition source.")
        val = key[1]
        if val not in alphabet:
            raise Exception("Invalid transition value.")
        for dest in transitions[key]:
            if dest not in states:
                raise Exception("Invalid transition destination.")
