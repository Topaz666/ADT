import heapq

class MyHuffman:
    def __init__(self):
        # Initialize the Huffman tree

        # dictionary to hold the characters and their coressponding bitcode
        self.chars = {}
        # Huffman tree
        self.tree = None
        # position in the bitstring being decoded
        self.decodePosition = 0

    def build(self, weights):
        # Build a huffman tree from the dictionary of character:value pairs
        pq = []
        for c, v in weights.items():
            pq.append(Node(v,c))
        heapq.heapify(pq)

        while len(pq) > 1:
            one = heapq.heappop(pq)
            two = heapq.heappop(pq)
            heapq.heappush(pq, Node(one.freq+two.freq,one.char+two.char,one,two))

        self.tree = pq[0]


    def makeLookupTable(self, node, bitCode):
        # Recursive algorithm to fill the dictionay of characters with their coressponding bitcode
        if node.left is None and node.right is None:
            self.chars[node.char]=bitCode
            return self
        else:
            if node.left:
                self.makeLookupTable(node.left,bitCode+'1')
            if node.right:
                self.makeLookupTable(node.right,bitCode+'0')

    def encode(self, word):
        # Return the bitstring of word encoded by the rules of your huffman tree
        self.makeLookupTable(self.tree, '')
        res = ''
        for c in word:
            if c in self.chars:
                res += self.chars[c]
        return res

    def decode(self, bitstring):
        # Return the word encoded in bitstring, or None if the code is invalid
        res = ''
        while len(bitstring) > 0:
            c,bs = self.recursiveTraverseTree(self.tree, bitstring)
            if bs == 0 and c == 0:
                return None
            res += c
            bitstring = bs
        return res

    def recursiveTraverseTree(self, node, bitString):
        # Return the character after traversing the Huffman tree through the bitstring
        if node.left is None and node.right is None:
            return node.char, bitString
        if bitString[0] == '1':
            return self.recursiveTraverseTree(node.left, bitString[1:])
        elif bitString[0] == '0':
            return self.recursiveTraverseTree(node.right, bitString[1:])
        else:
            return 0, 0
# This node structure might be useful to you
class Node:
    def __init__(self, value, data, left=None, right=None):
        self.char = data
        self.freq = value
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq <= other.freq

    def __gt__(self, other):
        return self.freq > other.freq

    def __ge__(self, other):
        return self.freq >= other.freq
