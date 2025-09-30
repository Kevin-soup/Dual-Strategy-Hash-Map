# Name: Kevin Lin
# OSU Email: link2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/5/2025
# Description: Implementation of an optimized HashMap using open addressing. Hash table collision is resolved
#              using open addressing with quadratic probing. The average case performance of user end operations
#              are maintained at an O(1) time complexity. An iterator implementation was also included.


from base_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Doubles HashMap table capacity when load factor is greater or equal to 0.5.
        """

        # Check if resize is needed.
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Find initial HashMap index.
        hash_value = self._hash_function(key)
        initial_index = hash_value % self._capacity

        # Use quadratic probe to find available index.
        for num in range(self._capacity):
            index = (initial_index + (num * num)) % self._capacity

            # Check if a HashEntry exist at index.
            if self._buckets[index] is None:

                # Create new HashEntry.
                self._buckets[index] = HashEntry(key, value)
                self._size += 1                                         # Update self._size.
                return

            # Check if index has a tombstone.
            elif self._buckets[index].is_tombstone:

                # Replace HashEntry information.
                self._buckets[index].key = key
                self._buckets[index].value = value
                self._buckets[index].is_tombstone = False
                self._size += 1                                         # Update self._size.
                return

            # Check if key already exist.
            elif self._buckets[index].key == key:

                # Replace existing value.
                self._buckets[index].value = value
                return


    def resize_table(self, new_capacity: int) -> None:
        """
        :param new_capacity: Integer value of the HashMap table's new capacity.

        Changes the underlying table's capacity. Active key-values are rehashed and put into a new table.
        If new_capacity is not a prime number, it will be set to the next highest prime number.
        """

        # If new_capacity is less current elements in hash map, method does nothing.
        if new_capacity < self._size:
            return

        # Ensure new_capacity is a prime number.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Store old information and create new HashMap table.
        old_table, old_capacity = self._buckets, self._capacity
        self._buckets = DynamicArray()

        for num in range(new_capacity):
            self._buckets.append(None)

        # Update capacity and size.
        self._capacity = new_capacity
        self._size = 0

        # Visit each HashMap index from the old table.
        for index in range(old_capacity):
            hash_entry = old_table[index]

            if hash_entry and hash_entry.is_tombstone is False:
                # Rehash active key-values to new table.
                self.put(hash_entry.key, hash_entry.value)


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

            # Check for active hash entry.
            if not self._buckets[index]:
                empty_buckets += 1

            # Check for active tombstone.
            elif self._buckets[index].is_tombstone is True:
                empty_buckets += 1

        return empty_buckets


    def get(self, key: str) -> object:
        """
        :param key: String that maps to an integer index of the HashMap.
        :return: Object paired to key.

        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """

        index = self._get_index_from_key(key)

        if index is not None:
            return self._buckets[index].value

        return None


    def contains_key(self, key: str) -> bool:
        """
        :param key: String that maps to an integer index of the HashMap.
        :return: True if key is in HashMap. False otherwise.

        Returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """

        index = self._get_index_from_key(key)

        if index is not None:
            return True

        return False


    def remove(self, key: str) -> None:
        """
        :param key: String that maps to an integer index of the HashMap.

        Removes given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """

        index = self._get_index_from_key(key)

        if index is not None:

            # Turn hash entry into tombstone.
            self._buckets[index].is_tombstone = True

            # Update self._size.
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
            hash_entry = self._buckets[index]

            # Check if hash map entry is empty or a tombstone
            if hash_entry and hash_entry.is_tombstone is False:

                # Append key-value pairs from HashEntry as tuples.
                contents_da.append((hash_entry.key, hash_entry.value))

        return contents_da


    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying table capacity.
        """

        # Point self._buckets to an empty dynamic array. Reset self._size.
        self._buckets = DynamicArray()
        self._size = 0

        # Add a none placeholder to each index, based on self._capacity.
        for index in range(self._capacity):
            self._buckets.append(None)


    def __iter__(self):
        """
        Creates iterator for HashMap loop.
        """

        self._index = 0

        return self


    def __next__(self):
        """
        Returns next value in HashMap and advances the iterator.
        """

        for num in range(self._index, self._capacity):
            hash_entry = self._buckets[num]
            self._index += 1

            # Check if hash_entry exists or a tombstone.
            if hash_entry is not None and hash_entry.is_tombstone is False:
                return hash_entry

        raise StopIteration


    def _get_index_from_key(self, key: str) -> int:
        """
        :param key: String that maps to an integer index of the HashMap.
        :return: Integer index associated with key.

        Returns the HashMap index that matches the key using quadratic probing.
        """

        hash_value = self._hash_function(key)
        initial_index = hash_value % self._capacity

        for num in range(self._capacity):
            index = (initial_index + (num * num)) % self._capacity

            # Check if hash map index is empty or a tombstone.
            if self._buckets[index] and self._buckets[index].is_tombstone is False:

                # Check for key.
                if self._buckets[index].key == key:
                    return index


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

