class CustomSymbolTable:
    def __init__(self, capacity=13):
        self.capacity = capacity
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def _hash(self, key):
        """
        Custom hash function: sum of ASCII values of key characters modulo capacity
        """
        if not isinstance(key, str):
            key = str(key)
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.capacity

    def add(self, key):
        index, position = self._find(key)
        if index != -1:
            return (index, position)
        else:
            index = self._hash(key)
            self.buckets[index].append(key)
            self.size += 1
            return (index, len(self.buckets[index]) - 1)

    def exists(self, key):
        index, _ = self._find(key)
        return index != -1

    def _find(self, key):
        index = self._hash(key)
        if index < len(self.buckets):
            for i, value in enumerate(self.buckets[index]):
                if value == key:
                    return (index, i)
        return (-1, -1)

    def __str__(self):
        result = ""
        for i in range(self.capacity):
            if self.buckets[i]:
                result += f'{i} -> {str(self.buckets[i])}\n'
        return result
