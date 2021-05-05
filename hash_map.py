# Course: CS261 - Data Structures
# Assignment: 5
# Student: Chris Hauser
# Description: Contains an implementation of a hash map data structure with methods to put in
# new key value pairs using the hash function, get and remove values for a certain key, check
# for a key in the map, count empty buckets, get an array of the keys in the map, resize the
# map capacity, clear the map, and calculate the table load. Built upon a dynamic array
# with singly linked lists for buckets.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Empties all the buckets in the hash map
        """
        # iterate through the buckets and set each to an empty SLL
        for i in range(self.capacity):
            self.buckets.set_at_index(i, LinkedList())

        self.size = 0
        return None

    def get(self, key: str) -> object:
        """
        If the key is present in the map, returns the value associated with the key. Returns None
        otherwise
        """
        # calculate the index for the key and grab it using contains from the bucket
        hash = self.hash_function(key)
        index = hash%self.capacity
        select = self.buckets.get_at_index(index).contains(key)
        # if it was found, return the value
        if select is not None:
            return select.value

        return None

    def put(self, key: str, value: object) -> None:
        """
        Calculates the correct index for the given key and places the key value pair in hte
        map at this index. If the key already exists, replaces the present value with the given
        value
        """
        # calculate the index and search the bucket at that index for a duplicate key
        hash = self.hash_function(key)
        index = hash % self.capacity
        bucket = self.buckets.get_at_index(index)
        dupe = bucket.contains(key)
        # if duplicate key exists, update value to given one
        if dupe is not None:
            dupe.value = value
            return None
        # otherwise, make a new key value pair and insert it into the bucket
        else:

            self.buckets.get_at_index(index).insert(key,value)
            self.size += 1
            return None

    def remove(self, key: str) -> None:
        """
        If the key is present in the map, removes the key and value from hte map. Does nothing
        if the key is not present
        """
        # calculate the index of the bucket
        hash = self.hash_function(key)
        index = hash%self.capacity
        # try to remove the node, reducing the size if successful
        if self.buckets.get_at_index(index).remove(key):
            self.size -= 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns a boolean reflecting if the given key is present in hte map
        """
        if self.empty_buckets() == self.capacity:
            return False
        # find the index of the bucket and search that bucket for the key
        hash = self.hash_function(key)
        index = hash%self.capacity
        # if a node was found, return True
        if self.buckets.get_at_index(index).contains(key) is not None:
            return True

        return False

    def empty_buckets(self) -> int:
        """
        Returns a count of the number of empty buckets in the entire hash map
        """
        tally = 0
        # iterate through the DA, incrementing the tally when an empty SLL is found
        for i in range(self.capacity):
            if self.buckets.get_at_index(i).head is None:
                tally += 1

        return tally

    def table_load(self) -> float:
        """
        Computes and returns the current table load of the hash map by dividing the
        number of elements by the current capacity
        """
        return self.size/self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash map and reindexes all of the previous keys into the new buckets
        """
        if new_capacity<1:
            return None

        # create new hashmap of new capacity
        newMap = HashMap(new_capacity,self.hash_function)
        # iterate through old buckets, putting each value into the new map
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            for node in bucket:
                newMap.put(node.key,node.value)
        #  set parameters to new buckets and capacity
        self.buckets = newMap.buckets
        self.capacity = new_capacity

        return None

    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array containing all the discrete keys present in the hash map
        """
        keys = DynamicArray()
        # iterate through the buckets
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            # iterate through the nodes in each bucket, adding the keys to the output array
            for node in bucket:
                keys.append(node.key)

        return keys


# BASIC TESTING
# if __name__ == "__main__":
#     m = HashMap(10, hash_function_2)
#     for i in range(100, 200, 10):
#         m.put(str(i), str(i * 10))
#
#     print(m)
#     print(m.get_keys())
#     m.resize_table(1)
#     print(m)
#     print(m.get_keys())
#     m.put('200', '2000')
#     m.remove('100')
#     m.resize_table(2)
#     print(m.get_keys())
# #
#     print("\nPDF - empty_buckets example 1")
#     print("-----------------------------")
#     m = HashMap(100, hash_function_1)
#     print(m.empty_buckets(), m.size, m.capacity)
#     m.put('key1', 10)
#     print(m.empty_buckets(), m.size, m.capacity)
#     m.put('key2', 20)
#     print(m.empty_buckets(), m.size, m.capacity)
#     m.put('key1', 30)
#     print(m.empty_buckets(), m.size, m.capacity)
#     m.put('key4', 40)
#     print(m.empty_buckets(), m.size, m.capacity)
#
#     #
#     print("\nPDF - empty_buckets example 2")
#     print("-----------------------------")
#     m = HashMap(50, hash_function_1)
#     for i in range(150):
#         m.put('key' + str(i), i * 100)
#         if i % 30 == 0:
#             print(m.empty_buckets(), m.size, m.capacity)
#
#
#     print("\nPDF - table_load example 1")
#     print("--------------------------")
#     m = HashMap(100, hash_function_1)
#     print(m.table_load())
#     m.put('key1', 10)
#     print(m.table_load())
#     m.put('key2', 20)
#     print(m.table_load())
#     m.put('key1', 30)
#     print(m.table_load())
#
#
#     print("\nPDF - table_load example 2")
#     print("--------------------------")
#     m = HashMap(50, hash_function_1)
#     for i in range(50):
#         m.put('key' + str(i), i * 100)
#         if i % 10 == 0:
#             print(m.table_load(), m.size, m.capacity)
#
#     print("\nPDF - clear example 1")
#     print("---------------------")
#     m = HashMap(100, hash_function_1)
#     print(m.size, m.capacity)
#     m.put('key1', 10)
#     m.put('key2', 20)
#     m.put('key1', 30)
#     print(m.size, m.capacity)
#     m.clear()
#     print(m.size, m.capacity)
#
#
#     print("\nPDF - clear example 2")
#     print("---------------------")
#     m = HashMap(50, hash_function_1)
#     print(m.size, m.capacity)
#     m.put('key1', 10)
#     print(m.size, m.capacity)
#     m.put('key2', 20)
#     print(m.size, m.capacity)
#     m.resize_table(100)
#     print(m.size, m.capacity)
#     m.clear()
#     print(m.size, m.capacity)
#
#
#     print("\nPDF - put example 1")
#     print("-------------------")
#     m = HashMap(50, hash_function_1)
#     for i in range(150):
#         m.put('str' + str(i), i * 100)
#         if i % 25 == 24:
#             print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
#
#
#     print("\nPDF - put example 2")
#     print("-------------------")
#     m = HashMap(40, hash_function_2)
#     for i in range(50):
#         m.put('str' + str(i // 3), i * 100)
#         if i % 10 == 9:
#             print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
#
#
#     print("\nPDF - contains_key example 1")
#     print("----------------------------")
#     m = HashMap(10, hash_function_1)
#     print(m.contains_key('key1'))
#     m.put('key1', 10)
#     m.put('key2', 20)
#     m.put('key3', 30)
#     print(m.contains_key('key1'))
#     print(m.contains_key('key4'))
#     print(m.contains_key('key2'))
#     print(m.contains_key('key3'))
#     m.remove('key3')
#     print(m.contains_key('key3'))
#
#
#     print("\nPDF - contains_key example 2")
#     print("----------------------------")
#     m = HashMap(75, hash_function_2)
#     keys = [i for i in range(1, 1000, 20)]
#     for key in keys:
#         m.put(str(key), key * 42)
#     print(m.size, m.capacity)
#     result = True
#     for key in keys:
#         # all inserted keys must be present
#         result &= m.contains_key(str(key))
#         # NOT inserted keys must be absent
#         result &= not m.contains_key(str(key + 1))
#     print(result)
#
#
#     print("\nPDF - get example 1")
#     print("-------------------")
#     m = HashMap(30, hash_function_1)
#     print(m.get('key'))
#     m.put('key1', 10)
#     print(m.get('key1'))
#
#
#     print("\nPDF - get example 2")
#     print("-------------------")
#     m = HashMap(150, hash_function_2)
#     for i in range(200, 300, 7):
#         m.put(str(i), i * 10)
#     print(m.size, m.capacity)
#     for i in range(200, 300, 21):
#         print(i, m.get(str(i)), m.get(str(i)) == i * 10)
#         print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
#
#
#     print("\nPDF - remove example 1")
#     print("----------------------")
#     m = HashMap(50, hash_function_1)
#     print(m.get('key1'))
#     m.put('key1', 10)
#     print(m.get('key1'))
#     m.remove('key1')
#     print(m.get('key1'))
#     m.remove('key4')
#
#
#     print("\nPDF - resize example 1")
#     print("----------------------")
#     m = HashMap(20, hash_function_1)
#     m.put('key1', 10)
#     print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
#     m.resize_table(30)
#     print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
#
#
#     print("\nPDF - resize example 2")
#     print("----------------------")
#     m = HashMap(75, hash_function_2)
#     keys = [i for i in range(1, 1000, 13)]
#     for key in keys:
#         m.put(str(key), key * 42)
#     print(m.size, m.capacity)
#
#     for capacity in range(111, 1000, 117):
#         m.resize_table(capacity)
#
#         m.put('some key', 'some value')
#         result = m.contains_key('some key')
#         m.remove('some key')
#
#         for key in keys:
#             result &= m.contains_key(str(key))
#             result &= not m.contains_key(str(key + 1))
#         print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))
#
#
#     print("\nPDF - get_keys example 1")
#     print("------------------------")
#     m = HashMap(10, hash_function_2)
#     for i in range(100, 200, 10):
#         m.put(str(i), str(i * 10))
#     print(m.get_keys())
#
#     m.resize_table(1)
#     print(m.get_keys())
#
#     m.put('200', '2000')
#     m.remove('100')
#     m.resize_table(2)
#     print(m.get_keys())
