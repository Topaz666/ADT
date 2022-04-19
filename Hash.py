    # PRIME1 = 127
    # PRIME2 = 113
    # hash1 = lambda a: a % PRIME1
    # hash2 = lambda a: PRIME2-(a%PRIME2)
class MyHashTable():
    def __init__(self, size, hash1):
    # Create an empty hashtable with the size given, and stores the function hash1
        self.table = [None]*size
        self.hashcode = hash1

    def put(self, key, data):
        # Store data with the key given, return true if successful or false if the data cannot be entered
        # On a collision, the table should not be changed
        tkey = self.hashcode(key)
        if self.table[tkey] is None:
            self.table[tkey] = [key,data]
        else:
            return False
        return True

    def get(self, key):
        # Returns the item linked to the key given, or None if element does not exist
        tkey = self.hashcode(key)
        if self.table[tkey] is not None and self.table[tkey][0] == key:
            return self.table[tkey][1]
        else:
            return None

    def __len__(self):
        # Returns the number of items in the Hash Table
        list = [x for x in self.table if x is not None]
        return len(list)

    def isFull(self):
        # Returns true if the HashTable cannot accept new members
        list = [x for x in self.table if x is None]
        if len(list) > 0:
            return False
        return True

class MyChainTable(MyHashTable):
    def __init__(self, size, hash1):
        # Create an empty hashtable with the size given, and stores the function hash1
        super().__init__(size,hash1)

    def put(self, key, data):
        # Store the data with the key given in a list in the table, return true if successful or false if the data cannot be entered
        # On a collision, the data should be added to the list
        tkey = self.hashcode(key)
        node = self.table[tkey]
        try:
            if node is None:
                self.table[tkey] = Node(key,data)
                return True
            while node.chain is not None:
                node = node.chain
            node.chain = Node(key,data)
        except:
            return False
        return True

    def get(self, key):
        # Returns the item linked to the key given, or None if element does not exist
        tkey = self.hashcode(key)
        node = self.table[tkey]
        while node is not None:
            if node.key == key:
                return node.data
            node = node.chain
        return None

    def __len__(self):
        # Returns the number of items in the Hash Table
        list = [x for x in self.table if x is not None]
        l = 0
        for i in list:
            node = i
            while node is not None:
                l += 1
                node = node.chain
        return l

    def isFull(self):
        # Returns true if the HashTable cannot accept new members
        return False

class MyDoubleHashTable(MyHashTable):
    def __init__(self, size, hash1, hash2):
        # Create an empty hashtable with the size given, and stores the functions hash1 and hash2
        super().__init__(size,hash1)
        self.hashcode2 = hash2

    def put(self, key, data):
        # Store data with the key given, return true if successful or false if the data cannot be entered
        # On a collision, the key should be rehashed using some combination of the first and second hash functions
        # Be careful that your code does not enter an infinite loop
        tkey = self.hashcode(key)
        tkey2 = self.hashcode2(key)
        i = 0
        tkey3 = self.hashcode(tkey + i*tkey2)
        try:
            if super().isFull():
                return False
            if self.table[tkey] is None:
                self.table[tkey] = [key,data]
                return True
            while self.table[tkey3] is not None:
                i += 1
                tkey3 = self.hashcode(tkey + i*tkey2)
            self.table[tkey3] = [key,data]
        except:
            return False
        return True

    def get(self, key):
        # Returns the item linked to the key given, or None if element does not exist
        tkey = self.hashcode(key)
        tkey2 = self.hashcode2(key)
        i = 1
        tkey3 = self.hashcode(tkey + i*tkey2)

        if self.table[tkey] is not None and self.table[tkey][0] == key:
            return self.table[tkey][1]

        while True:
            if tkey3 == tkey:
                return None
            tkey3 = self.hashcode(tkey + i*tkey2)
            if self.table[tkey3] is not None and self.table[tkey3][0] == key:
                return self.table[tkey3][1]
            i += 1

    def __len__(self):
        # Returns the number of items in the Hash Table
        return super().__len__()



class Node:
    def __init__(self, key, data, node=None):
        # Initialize this node, insert data, and set the next node if any
        self.key=key
        self.data=data
        self.chain=node
