from bloom_filter import BloomFilter
import hashlib
from bitarray import bitarray
import pickle

f = lambda x: bytes.fromhex(x.strip())

bf = BloomFilter(306259512, 0.005)
pickle_file = open('pickle_data', 'rb')
bf.bits = pickle.load(pickle_file)
pickle_file.close()
print('loaded pickled file')

q = None
while q != 'quit':
	q = input('?- ')
	a = hashlib.sha1(q.encode('utf-8')).hexdigest()
	query = f(a)
	print(bf.maybe_element(query))
