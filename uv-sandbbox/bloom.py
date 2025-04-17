#!/usr/bin/env python

import random


class BloomFilter:
    def __init__(self, size, num_hash_functions):
        self.size = size  # Number of bits in the filter
        self.num_hash_functions = num_hash_functions  # Number of hash functions to use
        self.bits = [False] * (size + 1)  # Using a list of booleans to represent bits

        # Initialize the random seeds for each hash function
        self.seeds = [random.randint(0, 999999) for _ in range(num_hash_functions)]

    def _hash_function(self, key, seed):
        """
        Generate an index in [1, size] using the key and a seed.
        """
        # Combine key and seed to create a unique hash
        hashed = (key * 7) + seed
        return hashed % self.size

    def add(self, key):
        """
        Add a key to the Bloom Filter by setting all its corresponding bits to True.
        """
        for i in range(self.num_hash_functions):
            index = self._hash_function(key, self.seeds[i])
            self.bits[index] = True

    def check(self, key):
        """
        Check if a key is possibly present in the Bloom Filter.
        Returns True (potential hit) or False (definitely not).
        """
        for i in range(self.num_hash_functions):
            index = self._hash_function(key, self.seeds[i])
            if not self.bits[index]:
                return False
        return True


# Example usage:
if __name__ == "__main__":
    # Create a Bloom Filter with 100 bits and 5 hash functions
    bf = BloomFilter(size=100, num_hash_functions=5)

    # Add some keys to the filter
    bf.add(1)
    bf.add(2)
    bf.add(3)

    # Check for cache hits/misses
    print(bf.check(1))  # Should return True (cache hit)
    print(bf.check(4))  # Should return False (cache miss)
