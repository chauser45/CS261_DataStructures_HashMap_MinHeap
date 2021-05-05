# Course: CS261 - Data Structures
# Assignment: 5
# Student: Chris Hauser
# Description: Contines an implementation of a min heap, with methods to add values, remove
# the minimum, and create a new minheap from an unsorted DA. Built upon a DA


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *



class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        Adds the given value to the heap, rearranging nodes to maintain min heap organization if
        necessary
        """
        index = self.heap.length()
        # add the new node to the end of the DA
        self.heap.append(node)
        # until the top is reached, compare the node with its parent and swap it if it is smaller
        while index != 0:
            parentIndex = ((index - 1) // 2)
            if self.heap.get_at_index(parentIndex) > node:
                self.heap.swap(index,parentIndex)
                index = parentIndex
            else:
                return None
        return None

    def get_min(self) -> object:
        """
        Returns the minimum value in the heap
        """
        if self.heap.length()==0:
            raise MinHeapException
        else:
            return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Returns an object with the minimum key from the heap, then reorganizes the heap as necessary
        to maintain organization
        """
        if self.heap.length() == 0:
            raise MinHeapException
        # for single node heaps, return the only value and remove it
        if self.heap.length() == 1:
            return self.heap.pop()
        # store the min value, remove the last value, then set the 0 index to the last value
        top = self.get_min()
        end = self.heap.pop()
        index = 0
        self.heap.set_at_index(index, end)
        # iterate until the node has no children
        while True:
            # calculat the indices of the node's children
            leftChildIndex = index * 2 + 1
            rightChildIndex = index * 2 + 2

            # grab the children if they are within the DA length
            leftChild = None
            if leftChildIndex < self.heap.length():
                leftChild = self.heap.get_at_index(leftChildIndex)
            rightChild = None

            if rightChildIndex < self.heap.length():
                rightChild = self.heap.get_at_index(rightChildIndex)

            # if the node has no children, we have percolated the node to its final position
            if leftChild is None and rightChild is None:
                return top
            # if no right child, compare and swap with left child if necessary
            if rightChild is None:
                if end > leftChild:
                    self.heap.swap(index, leftChildIndex)
                    index = leftChildIndex
                    # if the swap was made, keep going down
                    continue
                # if no swap was made, exit the loop and return the top value
                else:
                    return top
            # with two children, swap the node with its smallest child if one is smaller than it
            minChild = min(leftChild,rightChild)
            if end > minChild:
                if minChild == leftChild:
                    self.heap.swap(index,leftChildIndex)
                    index = leftChildIndex
                elif minChild == rightChild:
                    self.heap.swap(index,rightChildIndex)
                    index = rightChildIndex
            #  if done swapping, exit the loop and return the top value
            else:
                return top


    def build_heap(self, da: DynamicArray) -> None:
        """
        Rearranges a given DA to produce a valid min heap by percolating down subtrees starting
        with the first non leaf node
        """
        # for small inputs, no sorting is needed to form a heap
        if da.length == 0 or da.length() == 1:
            self.heap = da
            return None
        # calculate index of first non leaf node
        firstParentIndex = (da.length()-1)//2

        # index from this first parent back to the beginning of the array
        for outerIndex in range(firstParentIndex,-1,-1):
            subIndex = outerIndex
            # percolate the root of each subtree down in the same manner as when removing the minimum
            while True:
                subVal = da.get_at_index(subIndex)
                leftChildIndex = subIndex * 2 + 1
                rightChildIndex = subIndex * 2 + 2

                leftChild = None
                if leftChildIndex < da.length():
                    leftChild = da.get_at_index(leftChildIndex)
                rightChild = None

                if rightChildIndex < da.length():
                    rightChild = da.get_at_index(rightChildIndex)

                if leftChild is None and rightChild is None:

                    break
                if rightChild is None:
                    if subVal > leftChild:
                        da.swap(subIndex, leftChildIndex)
                        subIndex = leftChildIndex
                        continue
                    else:
                        break
                minChild = min(leftChild, rightChild)
                if subVal > minChild:
                    if minChild == leftChild:
                        da.swap(subIndex, leftChildIndex)
                        subIndex = leftChildIndex

                    else:
                        da.swap(subIndex, rightChildIndex)
                        subIndex = rightChildIndex
                else:
                    break
        self.heap = da

        return None


# BASIC TESTING
if __name__ == '__main__':
    #
    # print("\nPDF - add example 1")
    # print("-------------------")
    # h = MinHeap()
    # print(h, h.is_empty())
    # for value in range(300, 200, -15):
    #     h.add(value)
    #     print(h)
    #
    # print("\nPDF - add example 2")
    # print("-------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
    #     h.add(value)
    #     print(h)
    #
    #
    # print("\nPDF - get_min example 1")
    # print("-----------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # print(h.get_min(), h.get_min())

    #
    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())
    #
    #
    # print("\nPDF - build_heap example 1")
    # print("--------------------------")
    # da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    # h = MinHeap(['zebra', 'apple'])
    # print(h)
    # h.build_heap(da)
    # print(h)
    # da.set_at_index(0, 500)
    # print(da)
    # print(h)
