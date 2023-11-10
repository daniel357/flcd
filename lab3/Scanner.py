import re
from enum import Enum

from SymbolsTable import CustomSymbolTable

#
# def find_unbalanced_brace(braces_list):
#     stack = []
#
#     for index, brace in enumerate(braces_list):
#         if brace == '{':
#             stack.append(brace)
#         elif brace == '}':
#             if not stack or stack.pop() != '{':
#                 return brace  # Return the unbalanced brace
#
#     if len(stack) > 0:
#         return stack.pop()  # Return the first unbalanced brace that is still in the stack
#     else:
#         return None  # All braces are balanced


class Scanner:
    def __init__(self, file_info):
        self._lineCount = 0
        self._file = file_info
        self._SymbolTable = CustomSymbolTable()
        self._programInternalForm = []
        self._tokens = []
        # self._curly_braces_token = []
        try:
            self.readTokens()
            self.scan()
        except ValueError as err:
            print(err)

    def readTokens(self):
        with open("token.in") as token_file:
            for line in token_file:
                self._tokens.append(line.rstrip())

    def writeToFile(self):
        with open('PIF.out', 'w') as PIF_file:
            for element in self._programInternalForm:
                PIF_file.write(str(element) + '\n')

        with open('ST.out', 'w') as ST_file:
            ST_file.write("\nSymbol Table Constants & Identifiers\n")
            ST_file.write(str(self._SymbolTable))

    def scan(self):
        lines = re.split('[\n]', self._file)
        code_lines = []
        for line in lines:
            if line != ' ' and line != '':
                code_lines.append(line)
        for code_line in code_lines:
            line_tokens = self.tokenizeLine(code_line)

            for token in line_tokens:
                if token in self._tokens:
                    self._programInternalForm.append((token, 0))
                else:
                    if self.classifyToken(token) == 0:
                        raise ValueError(
                            "Lexical error: Token {} cannot be classified: line {}".format(token, self._lineCount))
                    if self.classifyToken(token) == 1:
                        self._SymbolTable.add(token)
                        self._programInternalForm.append(('identifier', (
                            self._SymbolTable.getPos(token)[0],
                            self._SymbolTable.getPos(token)[1])))
                    if self.classifyToken(token) == 2 or self.classifyToken(token) == 3 or self.classifyToken(
                            token) == 4:
                        self._SymbolTable.add(token)
                        self._programInternalForm.append(('constant', (
                            self._SymbolTable.getPos(token)[0],
                            self._SymbolTable.getPos(token)[1])))
        # unbalanced_brace = find_unbalanced_brace(self._curly_braces_token)
        # if unbalanced_brace is not None:
        #     raise ValueError(
        #         "Lexical error: Token {} cannot be classified".format(unbalanced_brace))
        self.writeToFile()
        print("Lexically corect")

    def tokenizeLine(self, line_string):
        self._lineCount += 1
        # split the line by everything that is not a list of alphanumeric values
        line_data = re.findall(r'("[^"]+"|[a-zA-Z0-9]+|[^a-zA-Z0-9"\s]+)', line_string)
        filtered_line_elements = []
        for element in line_data:
            if element is not None and element.strip() != '':
                filtered_line_elements.append(element)
        line_elements = filtered_line_elements
        print(filtered_line_elements)
        final_line_tokens = []
        i = 0
        n = len(line_elements)
        while i < n:
            if i > n:
                break
            if line_elements[i] == '=':
                if line_elements[i + 1] == '=':
                    final_line_tokens.append('==')
                    i = i + 1
                else:
                    final_line_tokens.append('=')
            elif line_elements[i] == '<':
                if line_elements[i + 1] == '>':
                    final_line_tokens.append('<' + line_elements[i + 1])
                    i = i + 1
                else:
                    final_line_tokens.append('<')
            elif line_elements[i] in '>':
                final_line_tokens.append('>')

            # elif line_elements[i] in ['{', '}']:
            #     self._curly_braces_token.append(line_elements[i])
            #     final_line_tokens.append(line_elements[i])
            else:
                final_line_tokens.append(line_elements[i])
            i = i + 1
        # print(final_line_tokens)
        return final_line_tokens

    def classifyToken(self, token):
        """
        Classify a token either as an identifier or a constant
        :param token:
        :return:
        """
        # identifier - letter{letter|digit} ->1
        match = re.match('^[a-zA-Z]+[a-zA-Z0-9]*$', token)
        if match is not None:
            return 1
        # constant
        # string constant - """{character}""" ->2
        # character - 'letter|digit' ->3
        # integer - "0"|["+"|"-"]nzDigit{digit} ->4
        string_match = re.match(r'^"[a-zA-Z0-9\s]+"$', token)
        if string_match is not None:
            return 2
        else:
            char_match = re.match('^\'[a-zA-Z0-9\'$]', token)
            if char_match is not None:
                return 3
            else:
                int_match = re.match('^0$|^(\+|-)?[1-9][0-9]*$', token)
                if int_match is not None:
                    return 4
        return 0
