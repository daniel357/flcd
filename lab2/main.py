from SymbolTable import CustomSymbolTable

# 2 symbol tables - 1 for identifiers, 1 for constants
if __name__ == '__main__':
    identifiersTable = CustomSymbolTable()
    identifiersTable.add('key')
    identifiersTable.add('hello')
    identifiersTable.add('world')
    identifiersTable.add('ad')
    identifiersTable.add('bc')
    identifiersTable.add('c')
    identifiersTable.add('d')
    identifiersTable.add(13)
    # print(identifiersTable._find('world'))
    # print(identifiersTable._find(13))
    # print(identifiersTable._find('nothing'))
    print(identifiersTable)
