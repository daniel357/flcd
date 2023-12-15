
class Parser:
    def __init__(self, grammar):
        """
        working stack: working stack alpha which stores the way the parse is built
        input_stack: input stack beta which is a part of the tree to be built
        state: state of the parsing which can take one of the following values:
            • q = normal state
            • b = back state
            • f = final state - corresponding to success: w ε L(G)
            • e = error state – corresponding to insuccess: w ∉ L(G)
         i: position of current symbol in input sequence
        :param grammar: grammar of the language for which we will perform the sequence check
        """
        self._grammar = grammar
        self._working_stack = []
        self._input_stack = [self._grammar.start_sym()]
        self._state = "q"
        self._index = 0

    def getState(self):
        return self._state

    def setState(self, value):
        self._state = value

    def getIndex(self):
        return self._index

    def setIndex(self, value):
        self._index = value

    def getWorkingStack(self):
        return self._working_stack

    def setWorkingStack(self, stack):
        self._working_stack = stack

    def getInputStack(self):
        return self._input_stack

    def setInputStack(self, stack):
        self._input_stack = stack

    def expand(self):
        """
        Occurs when the head of the stack is a non-terminal
        1. pop non-terminal from the input stack
        2. add Ai to the working stack alpha
        3. Get the first production of A
        4. Add the corresponding production to the input stack
        :return:
        """
        nonTerminal = self._input_stack.pop(0)
        production = self._grammar.productions_for(nonTerminal)[0]
        self._working_stack.append((nonTerminal, production[1]))
        production_elems = production[0].split('$')
        self._input_stack = production_elems + self._input_stack

    def advance(self):
        """
        WHEN: head of input stack is a terminal = current symbol from input
        1. get the top of the input stack
        2. add it to the working stack
        3. increase index i
        :return:
        """
        nonTerminal = self._input_stack.pop(0)
        print(self._input_stack)
        self._working_stack.append(nonTerminal)  # step 2
        self._index += 1  # step 3

    def momentaryInsuccess(self):
        """
        WHEN: head of input stack is a terminal ≠ current symbol from input
        1.State becomes back.
        :return:
        """
        self._state = "b"  # step 1

    def back(self):
        """
        WHEN: head of working stack is a terminal
        Steps:
        1. get the last element from the working stack
        2. add it back to the input stack
        3. decrease index
        :return:
        """
        last = self._working_stack.pop()  # step 1
        self._input_stack = [last] + self._input_stack  # step 2
        self._index -= 1  # step 3

    def anotherTry(self):
        """
        WHEN: head of working stack is a non-terminal

        Steps:

        1. get the top of the working stack: tuple of form (non_terminal, production_nr)
        2. check if we have more productions for that non-terminal
            2.1. update the state as 'q': normal state
            2.2. create a new tuple consisting of (non_terminal, production_nr+1) and add it to the working stack
                 (moving on to the next production)
            2.3. Update the top of input stack with the new production: delete old one and replace it
            2.4. Slice the list to delete last production
            2.5. Insert the new one on top
        3. if there are no more productions for the current terminal we check the following condition:

        4. otherwise, delete the last production from the working stack and put the corresponding non-terminal in the
           input stack

        :return:
        """
        last = self._working_stack.pop()
        if self._grammar.has_additional_production(last[0], last[1]):
            self._state = "q"
            self._working_stack.append((last[0], last[1] + 1))
            production_elems = self._grammar.specific_production(last[0], last[1])
            lastLength = len(production_elems[0].split('$'))
            self._input_stack = self._input_stack[lastLength:]
            production_elems = self._grammar.specific_production(last[0], last[1] + 1)[0]
            self._input_stack = production_elems.split('$') + self._input_stack
        elif self._index == 0 and last[0] == self._grammar.start_sym():
            self._state = "e"
        else:
            production_elems = self._grammar.specific_production(last[0], last[1])
            lastLength = len(production_elems[0].split('$'))

            self._input_stack = self._input_stack[lastLength:]
            self._input_stack = [last[0]] + self._input_stack

    def success(self):
        """
        1. Mark the state as final
        :return:
        """
        self._state = "f"
