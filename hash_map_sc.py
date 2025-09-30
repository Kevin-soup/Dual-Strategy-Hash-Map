# Name: Kevin Lin
# OSU Email: link2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/5/2025
# Description: Implementation of an optimized HashMap using linked list chaining. The hash table is stored in
#              a dynamic array and collisions are resolved using a singly linked list. The average case
#              performance of user end operations are maintained at an O(1) time complexity.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        :param key: String that maps to an integer index of the HashMap.
        :param value: Object to be added to the mapped location.

        Updates key-value pair in the hash map. If key is not in the hash map, adds new key-value pair.
        Doubles HashMap table capacity when load factor is greater or equal to 1.
        """

        # Check if resize is needed.
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Find HashMap index.
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # Check if a key-value pair already exist at HashMap index.
        linked_list = self._buckets[index]
        node = linked_list.contains(key)

        if node:
            # Replace existing value.
            node.value = value

        else:
            # Add new key-value pair and update self._size.
            linked_list.insert(key, value)
            self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """
        :param new_capacity: Integer value of the HashMap table's new capacity.

        Changes the underlying table's capacity. Existing key-values are rehashed and put into a new table.
        If new_capacity is not a prime number, it will be set to the next highest prime number.
        """

        # If new_capacity is less than one, method does nothing.
        if new_capacity < 1:
            return

        # Ensure new_capacity is a prime number.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Store old information and create new HashMap table.
        old_table, old_capacity = self._buckets, self._capacity
        self._buckets = DynamicArray()

        for num in range(new_capacity):
            self._buckets.append(LinkedList())

        # Update capacity and size.
        self._capacity = new_capacity
        self._size = 0

        # Visit each HashMap index from the old table.
        for index in range(old_capacity):
            linked_list = old_table[index]

            # Rehash key-values to new table.
            for node in linked_list:
                self.put(node.key, node.value)


    def table_load(self) -> float:
        """
        Returns the load factor of current HashMap table.
        Load Factor = objects stored / number of buckets
        """

        return self._size / self._capacity


    def empty_buckets(self) -> int:
        """
        :return: Integer of empty buckets.

        Returns the number of empty buckets in the hash table.
        """

        empty_buckets = 0

        # Visit each HashMap index.
        for index in range(self._capacity):

            # Check if bucket is empty.
            if self._buckets[index].length() == 0:
                empty_buckets += 1

        return empty_buckets


    def get(self, key: str) -> object:
        """
        :param key: String that maps to an integer index of the HashMap.
        :return: Object paired to key.

        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """

        node = self._get_node_from_key(key)

        if node:
            return node.value

        return None


    def contains_key(self, key: str) -> bool:
        """
        :param key: String that maps to an integer index of the HashMap.
        :return: True if key is in HashMap. False otherwise.

        Returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """

        if self._get_node_from_key(key):
            return True

        return False


    def remove(self, key: str) -> None:
        """
        :param key: String that maps to an integer index of the HashMap.

        Removes given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """

        # Find HashMap index.
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # Check for key in linked list nodes.
        linked_list = self._buckets[index]

        # Remove node with key. Update self._size.
        if linked_list.remove(key):
            self._size -= 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        :return: Dynamic array of key-value pairs.

        Returns a dynamic array where each index contains a tuple of a key-value pair from the hash map.
        """

        # Create new dynamic array.
        contents_da = DynamicArray()

        # Visit each HashMap index.
        for index in range(self._capacity):
            linked_list = self._buckets[index]

            # Append key-value pairs from linked list nodes as tuples.
            for node in linked_list:
                contents_da.append((node.key, node.value))

        return contents_da


    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying table capacity.
        """

        # Point self._buckets to an empty dynamic array. Reset self._size.
        self._buckets = DynamicArray()
        self._size = 0

        # Add a linked list to each index, based on self._capacity.
        for index in range(self._capacity):
            self._buckets.append(LinkedList())


    def _get_node_from_key(self, key: str) -> object:
        """
        :param key: String that maps to an integer index of the HashMap.
        :return: SLNode associated with key.

        Returns the node that matches the key. If key is not found, returns None.
        """

        # Find HashMap index.
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # Check for key in linked list nodes.
        linked_list = self._buckets[index]
        return linked_list.contains(key)


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    :param da: Unsorted DynamicArray of strings.
    :return: Tuple (DynamicArray of the mode, integer representing the mode's frequency).

    Returns a tuple of the mode in a DynamicArray and it's frequency.
    If more than one value has the highest frequency, all values at frequency should be in the array.
    """

    # Create a HashMap with key = string from dynamic array ; value = occurrence.
    map = HashMap()

    for index in range(da.length()):

        # If key already exist, increment the value.
        if map.contains_key(da[index]):
            map.put(da[index], map.get(da[index]) + 1)
        else:
            map.put(da[index], 1)

    # Retrieve all keys and values from HashMap.
    mapped_da = map.get_keys_and_values()

    # Check for highest frequency.
    top_frequency = 0

    for index in range(mapped_da.length()):
        key, value = mapped_da[index]

        if value > top_frequency:
            top_frequency = value

    # Create dynamic array containing the mode(s).
    mode_da = DynamicArray()

    for index in range(mapped_da.length()):
        key, value = mapped_da[index]

        if value == top_frequency:
            mode_da.append(key)

    return mode_da, top_frequency


# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
