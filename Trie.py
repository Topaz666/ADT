class MyTrie:
    def __init__(self):
        # Initialize the trie node as needed
        self.children_links = [None] * 54
        self.TERMINAL = 0

    def char_to_position(self, c):
        # index 0 is the TERMINAL flag
        # index 1 is the apostrophe (')
        # index 2-27 is A-Z
        # index 28-53 is a-a
        if c == "'":
            return 1
        elif c == "#":
            return 0
        elif "A" <= c <= "Z":
            return 2 + ord(c) - ord("A")
        elif "a" <= c <= "z":
            return 28 + ord(c) - ord("a")
        return -1

    def insert(self, word, position=0):
        # Insert word into the correct place in the trie
        p = self
        if len(word) > position:
            index = p.char_to_position(word[position])
            if p.children_links[index] is None:
                p.children_links[index] = word
            elif type(p.children_links[index]) == str:
                l = p.children_links[index]
                p.children_links[index] = MyTrie()
                p = p.children_links[index]
                p.insert(l,position+1)
                p.insert(word, position+1)
            elif type(p.children_links[index]) == MyTrie:
                p = p.children_links[index]
                p.insert(word, position+1)
        elif type(p) == MyTrie:
            p.children_links[p.TERMINAL] = word

    def remove(self, word, position=0):
        # Find and remove the node that contains the word
        p = self
        if len(word) > position:
            index = p.char_to_position(word[position])
            if p.children_links[index] is None:
                return -1
            elif type(p.children_links[index]) == str and p.children_links[index] == word:
                p.children_links[index] = None
                return 1
            elif type(p.children_links[index]) == MyTrie:
                x = p.children_links[index]
                res = x.remove(word, position + 1)
                if res > 0:
                    list = [z for z in x.children_links if z is not None]
                    if len(list) < 1:
                        del(p.children_links[index])
                        p.children_links[index] = None
                        return 1
                    return 0
                return res
        elif type(p) == MyTrie and p.children_links[p.TERMINAL] == word:
            p.children_links[p.TERMINAL] = None
            return 1
        else:
            return -1

    def depth_of_word(self, word, position=0):
        # Return the depth of the node that contains the word
        p = self
        if len(word) > position:
            index = p.char_to_position(word[position])
            if p.children_links[index] is None:
                return -1
            elif type(p.children_links[index]) == str:
                return position + 1
            elif type(p.children_links[index]) == MyTrie:
                p = p.children_links[index]
                return p.depth_of_word(word, position+1)
        elif type(p.children_links[P.TERMINAL]) == str:
                return positon + 1
        else:
            return -1

    def exists(self, word, position=0):
        # Return true if the passed word exists in this trie node
        p = self
        if len(word) > position:
            index = p.char_to_position(word[position])
            if p.children_links[index] is None:
                return False
            elif type(p.children_links[index]) == str and p.children_links[index] == word:
                return True
            p = p.children_links[index]
            return p.exists(word,position+1)
        elif type(p) == MyTrie and p.children_links[p.TERMINAL] == word:
            return True
        else:
            return False

    def autoComplete(self, prefix, position=0):
        # Return every word that extends this prefix in alphabetical order
        p = self
        res = []
        def backtrace(p):
            for x in p.children_links:
                if x is None:
                    continue
                if type(x) == str:
                    res.append(x)
                elif type(x) == MyTrie:
                    p = x
                    backtrace(p)
            return
        if len(prefix) > position:
            index = p.char_to_position(prefix[position])
            if p.children_links[index] is None:
                return []
            elif type(p.children_links[index]) == str and p.children_links[index][0:len(prefix)] == prefix:
                return [p.children_links[index]]
            elif type(p.children_links[index]) == MyTrie:
                p = p.children_links[index]
                return p.autoComplete(prefix, position + 1)
        else:
            backtrace(p)
            return res
