class MyBST:
    def __init__(self, data, promote_right=True):
        # Initialize this node, and store data in it
        self.data = data
        self.left = None
        self.right = None
        self.height = 0

        # Set promote_right to TRUE if you are implementing
        # the promotion of the smallest node on left subtree,
        # Otherwise, set it to FALSE
        self.promote_right = promote_right

    def getLeft(self):
        # Return the left child of this node, or None
        return self.left

    def getRight(self):
        # Return the right child of this node, or None
        return self.right

    def getData(self):
        # Return the data contained in this node
        return self.data

    def getHeight(self):
        # Return the height of this node
        return self.height

    def updateHeight(self):
        # Update the height of this node
        if self.left is None:
            left_height = 0
        else:
            left_height = self.left.updateHeight()+1
        if self.right is None:
            right_height = 0
        else:
            right_height = self.right.updateHeight()+1
        self.height = max(left_height,right_height)
        return self.height

    def __contains__(self, data):
        # Returns true if data is in this node or a node descending from it
        if data > self.data:
            if self.right is None: return False
            return self.right.__contains__(data)
        elif data < self.data:
            if self.left is None: return False
            return self.left.__contains__(data)
        return True

    def insert(self, data):
        # Insert data into the tree, descending from this node
        # Ensure that the tree remains a valid Binary Search Tree
        # Return this node after data has been inserted
        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.left = MyBST(data)
        else:
            if self.right:
                self.right.insert(data)
            else:
                self.right = MyBST(data)
        self.updateHeight()
        return self

    def findSmallest(self):
        # Return the value of the smallest node
        if self.left:
            return self.left.findSmallest()
        return self.data

    def findLargest(self):
        # Return the value of the largest node
        if self.right:
            return self.right.findLargest()
        return self.data

    def remove(self, data):
        # Remove find the data in the input parameter and remove it
        # Ensure that the tree remains a valid Binary Search Tree
        # Return this node after data has been inserted
        if data < self.data:
            if self.left is None: return self
            self.left = self.left.remove(data)
        elif data > self.data:
            if self.right is None: return self
            self.right = self.right.remove(data)
        else:
            if self.left is None and self.right is None:
                self = None
                return self
            elif self.left is None:
                temp = self.right
                self = None
                return temp
            elif self.right is None:
                temp = self.left
                self = None
                return temp
            else:
                if self.promote_right:
                    temp = self.right.findSmallest()
                    self.data = temp
                    self.right = self.right.remove(temp)
                else:
                    temp = self.left.findLargest()
                    self.data = temp
                    self.left = self.left.remove(temp)
        self.updateHeight()
        return self


class MyAVL(MyBST):
    def __init__(self, data):
        # Initialize this node, and store data in it
        super().__init__(data)
        self.bf = 0

    def reBalance(self):
        # Check to see if the current node is out of balance
        # Rebalance it if necessary
        if self.bf > 1:
            self.left.bf = self.left.getBalanceFactor()
            if self.left.bf < 0:
                self.left = self.left.leftRotate()
                self = self.rightRotate()
            else:
                self = self.rightRotate()
        elif self.bf < -1:
            self.right.bf = self.right.getBalanceFactor()
            if self.right.bf > 0:
                self.right = self.right.rightRotate()
                self = self.leftRotate()
            else:
                self = self.leftRotate()
        return self

    def getBalanceFactor(self):
        # Return the balance factor of this node
        if self.left:
            left_height = self.left.height
        else:
            left_height = -1
        if self.right:
            right_height = self.right.height
        else:
            right_height = -1
        return left_height - right_height

    def insert(self, data):
        # Insert data into the tree, descending from this node
        # Ensure that the tree remains a valid AVL tree
        # Return the node in this node's position after data has been inserted
        if data < self.data:
            if self.left:
                self.left = self.left.insert(data)
            else:
                self.left = MyAVL(data)
        else:
            if self.right:
                self.right = self.right.insert(data)
            else:
                self.right = MyAVL(data)
        self.updateHeight()
        self.bf = self.getBalanceFactor()
        new = self.reBalance()
        return new

    def leftRotate(self):
        # Perform a left rotation on this node and return the new node in its spot
        new = self.getRight()
        self.right = new.getLeft()
        new.left = self
        new.left.updateHeight()
        new.updateHeight()
        return new

    def rightRotate(self):
        # Perform a right rotation on this node and return the new node in its spot
        new = self.getLeft()
        self.left = new.getRight()
        new.right = self
        new.right.updateHeight()
        new.updateHeight()
        return new

    def remove(self, data):
        # Remove find the data in the input parameter and remove it
        # Ensure that the tree remains a valid AVL tree
        # Return the node in this node's position after data has been inserted
        if data < self.data:
            if self.left is None: return self
            self.left = self.left.remove(data)
        elif data > self.data:
            if self.right is None: return self
            self.right = self.right.remove(data)
        else:
            if self.left is None and self.right is None:
                self = None
                return self
            elif self.left is None:
                temp = self.right
                self = None
                return temp
            elif self.right is None:
                temp = self.left
                self = None
                return temp
            else:
                if self.promote_right:
                    temp = self.right.findSmallest()
                    self.data = temp
                    self.right = self.right.remove(temp)
                else:
                    temp = self.left.findLargest()
                    self.data = temp
                    self.left = self.left.remove(temp)
        self.updateHeight()
        self.bf = self.getBalanceFactor()
        self = self.reBalance()
        return self


# Bonus functions to help you debug
def printTree_(tree, prefix):
    if tree.getLeft() is not None:
        printTree_(tree.getLeft(), prefix + "+ ")
    print(f"{prefix}{tree.data}")
    if tree.getRight() is not None:
        printTree_(tree.getRight(), prefix + "- ")


def printTree(tree):
    printTree_(tree, "")
