import typing as t
from typing import Iterator, Optional, Tuple, List, TypeVar, Generic

# Define the structure for a node in the hash table, 
# which is (key, value) inside a list (the bucket/chain).
K = TypeVar('K')
V = TypeVar('V')
Bucket = List[Tuple[K, V]]


class Hashtable(Generic[K, V]):
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
        self._buckets: List[Bucket] = [[] for _ in range(self._capacity)]
        self._size: int = 0  # Number of key-value mappings
        self.load_factor: float = load_factor

    def _hash(self, key: K) -> int:
        """
        Calculates the index for the given key.
        Uses the built-in hash function and the modulo operator.
        """
        return hash(key) % self._capacity

    def put(self, key: K, value: V) -> Optional[V]:
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

    def get(self, key: K, default: Optional[V] = None) -> V:
        """
        Returns the value to which the specified key is mapped.
        If the key is not found, returns the optional 'default' value 
        or raises KeyError if 'default' is not provided.
        
        This implements the more flexible Python 'dict.get(key, default)' signature.
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value
        
        # Key not found in the bucket chain. Return default or raise error.
        if default is not None:
            return default
            
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
            # Use the simple get() implementation (without default) to check for existence
            self.get(key, default=None) 
            return True
        except KeyError:
            return False

    def contains_value(self, value: V) -> bool:
        """
        Checks if the specified value exists in the hash table.
        Note: This requires checking every item (O(N) complexity).
        """
        for _, v in self.items():
            if v == value:
                return True
        return False
        
    def is_empty(self) -> bool:
        """
        Returns true if this hash table contains no key-value mappings.
        """
        return self._size == 0

    def clear(self):
        """
        Removes all of the mappings from this hash table.
        """
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        print("--- INFO: Hashtable cleared ---")

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
                # put() handles the new hashing and size update
                self.put(key, value) 
        
        print(f"--- INFO: Hashtable resized from {old_capacity} to {self._capacity} ---")

    # --- Pythonic Iterator Methods (Views) ---

    def keys(self) -> Iterator[K]:
        """
        Returns an iterator over the keys in the hash table.
        """
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def values(self) -> Iterator[V]:
        """
        Returns an iterator over the values in the hash table.
        """
        for bucket in self._buckets:
            for _, value in bucket:
                yield value

    def items(self) -> Iterator[Tuple[K, V]]:
        """
        Returns an iterator over the (key, value) pairs (items) in the hash table.
        """
        for bucket in self._buckets:
            for key, value in bucket:
                yield (key, value)

    def __iter__(self) -> Iterator[K]:
        """
        Allows iteration over keys: for key in hashtable:
        """
        return self.keys()

    # --- Pythonic Interface Methods (Magic Methods) ---

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
        Note: If using Pythonic indexing (like dict[key]), we must raise 
        KeyError if not found, not return None. We use the 'get' method 
        without the default parameter for this.
        """
        # Call the dedicated get method, which raises KeyError
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
        for key, value in self.items():
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
    
    print(f"Initial State: {map!r}. Is empty? {map.is_empty()}")
    
    map.put("name", "Alice")
    map.put(101, "Java")
    map.put(3.14, "Pi")
    
    # Check new size methods
    print(f"\nState after 3 puts: {map!r}. Size: {len(map)}")
    
    # Resizing check (4th item triggers resize as 4 > 4 * 0.75 = 3)
    map["apple"] = "Fruit" 
    
    print(f"\nState after resize: {map!r}")
    
    # Check iteration methods
    print("\nIterating over keys:")
    for key in map.keys():
        print(f"- Key: {key}")
        
    print("Iterating over items:")
    for key, value in map.items():
        print(f"- {key} -> {value}")
        
    # Check contains_value
    print(f"\nContains value 'Fruit'? {map.contains_value('Fruit')}")
    print(f"Contains value 'Zebra'? {map.contains_value('Zebra')}")
    
    # Check get with default
    print(f"Get 'missing' with default 'N/A': {map.get('missing', 'N/A')}")
    
    # Clear the map
    map.clear()
    print(f"\nState after clear: {map!r}. Is empty? {map.is_empty()}")

    # Attempt to access non-existent key after clear
    try:
        map['name']
    except KeyError as e:
        print(f"Caught expected error: {e}")