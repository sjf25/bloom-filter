import math
import bitarray
import mmh3

class BloomFilter:
	# sets the optimal number of hash functions and size of filter
	# according to expected number of elements and desired false positive probability
	def __init__(self, expected_n, desired_p, hash_func = mmh3.hash):
		m = int(-expected_n * math.log(desired_p) / math.log(2)**2)
		self.k = int(-math.log(desired_p) / math.log(2))
		self.bits = bitarray.bitarray(m)
		self.bits.setall(0)
		self.hash_func = hash_func
	
	# uses the Kirsch-Mitzenmacher-Optimization to compute hashes
	# see: https://www.eecs.harvard.edu/~michaelm/postscripts/tr-02-05.pdf
	def get_indices(self, obj):
		bit_count = len(self.bits)
		hash_0 = self.hash_func(obj, 0)
		hash_1 = self.hash_func(obj, 1)
		return ((hash_0 + i*hash_1) % bit_count for i in range(self.k))

	def add(self, obj):
		for index in self.get_indices(obj):
			self.bits[index] = 1

	# checks if an element may be in the filter
	# may return false positives
	def maybe_element(self, obj):
		for index in self.get_indices(obj):
			if self.bits[index] == 0:
				return False
		return True
