import math
import bitarray
import mmh3

class BloomFilter:
	# sets the optimal number of hash functions and size of filter
	# according to expected number of elements and desired false positive probability
	def __init__(self, expected_n = 0, desired_p = 0, hash_func = mmh3.hash):
		self.hash_func = hash_func
		if expected_n == 0:
			return
		m = int(-expected_n * math.log(desired_p) / math.log(2)**2)
		self.k = int(-math.log(desired_p) / math.log(2))
		self.bits = bitarray.bitarray(m)
		self.bits.setall(0)
	
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
	
	def write(self, write_file):
		# write the number of padding bits
		padding_count = (8 - len(self.bits) % 8) % 8
		write_file.write(bytes([padding_count]))
		# write the value of k 
		# assumes k is less than 256 which is reasonable
		# TODO: catch exception
		write_file.write(bytes([self.k]))
		# write the bitarray
		self.bits.tofile(write_file)
		write_file.close()
	
	def open(read_file):
		# read the number of padding bits
		padding_count = int.from_bytes(read_file.read(1), byteorder='little')
		bits = bitarray.bitarray(0)
		# read k (assumes fits in one byte
		k = int.from_bytes(read_file.read(1), byteorder='little')
		# read the bit array
		bits.fromfile(read_file)
		read_file.close()
		# trim the padding bits
		del bits[-padding_count:]
		
		opened_bf = BloomFilter()
		opened_bf.bits = bits
		opened_bf.k = k
		return opened_bf
