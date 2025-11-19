import typing as t

# Define the structure for a node in the hash table, 
# which is (key, value) inside a list (the bucket/chain).
K = t.TypeVar('K')
V = t.TypeVar('V')
Bucket = t.List[t.Tuple[K, V]]


class Hashtable(t.Generic[K, V]):
    """
    A custom Python implementation of a hash table structure, 
    mimicking key features found in Java's Hashtable, including 
    separate chaining for collision resolution and dynamic resizing.
    
    Data is stored in buckets (lists of key-value pairs).
    """

    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75):
        """
        Initializes the hash table.
        
        Args:
            initial_capacity: The initial number of buckets. Must be >= 1.
            load_factor: The ratio of (size / capacity) at which the table resizes.
        """
        if initial_capacity < 1:
            raise ValueError("Capacity must be at least 1")
            
        self._capacity: int = initial_capacity
        # The main array of buckets (using a list of lists/chains)
        self._buckets: t.List[Bucket] = [[] for _ in range(self._capacity)]
        self._size: int = 0  # Number of key-value mappings
        self.load_factor: float = load_factor

    def _hash(self, key: K) -> int:
        """
        Calculates the index for the given key.
        Uses the built-in hash function and the modulo operator.
        """
        return hash(key) % self._capacity

    def put(self, key: K, value: V) -> t.Optional[V]:
        """
        Maps the specified key to the specified value in this hash table.
        
        If the key already exists, the old value is returned and the new 
        value is stored. Otherwise, None is returned.
        
        Args:
            key: The key to be hashed.
            value: The value associated with the key.
        """
        index = self._hash(key)
        bucket = self._buckets[index]
        
        # 1. Search for existing key (Update case)
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                old_value = bucket[i][1]
                # Replace the old (key, value) tuple with the new one
                bucket[i] = (key, value)
                return old_value

        # 2. Key not found (Insert case)
        bucket.append((key, value))
        self._size += 1

        # 3. Check for resizing/rehash
        if self._size > self._capacity * self.load_factor:
            self._rehash()

        return None

    def get(self, key: K) -> V:
        """
        Returns the value to which the specified key is mapped.
        Raises KeyError if the key is not found (Pythonic behavior).
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value
        
        # Key not found in the bucket chain
        raise KeyError(f"Key not found: {key}")

    def remove(self, key: K) -> V:
        """
        Removes the key (and its corresponding value) from the hash table.
        Returns the value that was removed. Raises KeyError if not found.
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for i, (existing_key, value) in enumerate(bucket):
            if existing_key == key:
                # Remove the element at index i from the bucket list
                del bucket[i]
                self._size -= 1
                return value
        
        # Key not found in the bucket chain
        raise KeyError(f"Key not found: {key}")

    def contains_key(self, key: K) -> bool:
        """
        Checks if the specified key is mapped in the hash table.
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def _rehash(self):
        """
        Doubles the capacity and re-inserts all existing key-value pairs.
        This is a common method for dynamic hash table resizing.
        """
        old_capacity = self._capacity
        old_buckets = self._buckets
        
        # Double the capacity
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0 # Size will be rebuilt during re-insertion

        # Re-insert all elements into the new, larger bucket array
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value) # put() handles the new hashing and size update
        
        print(f"--- INFO: Hashtable resized from {old_capacity} to {self._capacity} ---")

    # --- Pythonic Interface Methods ---

    def __len__(self) -> int:
        """
        Implements len(hashtable)
        """
        return self._size

    def __setitem__(self, key: K, value: V):
        """
        Implements hashtable[key] = value
        """
        self.put(key, value)

    def __getitem__(self, key: K) -> V:
        """
        Implements value = hashtable[key]
        """
        return self.get(key)

    def __delitem__(self, key: K):
        """
        Implements del hashtable[key]
        """
        self.remove(key)

    def __contains__(self, key: K) -> bool:
        """
        Implements key in hashtable
        """
        return self.contains_key(key)

    def __str__(self) -> str:
        """
        Provides a string representation of the hash table contents.
        """
        items = []
        for bucket in self._buckets:
            for key, value in bucket:
                items.append(f"{repr(key)}: {repr(value)}")
        return "{" + ", ".join(items) + "}"
    
    def __repr__(self) -> str:
        """
        Provides a detailed string representation.
        """
        return f"Hashtable(size={self._size}, capacity={self._capacity})"

# --- Example Usage ---

if __name__ == '__main__':
    # Initialize a small hashtable to easily demonstrate resizing
    map = Hashtable(initial_capacity=4, load_factor=0.75) 
    
    print(f"Initial State: {map!r}")
    
    map.put("name", "Alice")
    map.put(101, "Java")
    map.put(3.14, "Pi")
    
    print(f"State after 3 puts: {map!r}")
    print(f"Value for 'name': {map.get('name')}")
    print(f"Contains 'name'? {map.contains_key('name')}")
    
    # Trigger collision (keys 'name' and 'omen' might collide on a small table, 
    # but we'll just add more unique items)
    map[5] = "Five"
    
    # Capacity is 4. Load factor is 0.75. Resize triggers when size > 4 * 0.75 = 3.
    # Current size is 4. Resizing should trigger here:
    map["apple"] = "Fruit" 
    
    print(f"\nState after resize: {map!r}")
    
    # Update an existing key
    old = map.put(101, "Python")
    print(f"\nUpdated 101. Old value: {old}")
    print(f"New value for 101: {map[101]}")
    
    # Remove a key
    removed_value = map.remove(5)
    print(f"\nRemoved key 5. Value removed: {removed_value}")
    print(f"Current size: {len(map)}")
    
    # Demonstrate Pythonic deletion
    del map['apple']
    print(f"State after del: {map!r}")

    # Attempt to access non-existent key
    try:
        map['missing']
    except KeyError as e:
        print(f"\nCaught expected error: {e}")