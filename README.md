# Bloom Filter
## What is a Bloom Filter?
A bloom filter is a space-efficient probablistic data structure used to check set membership. For more information, see: <https://en.wikipedia.org/wiki/Bloom_filter>

## How to use
```python
from bloom_filter import BloomFilter

# the constructor takes the expected number of elements and the desired error probability
number_of_elements = 1000
desired_error = 0.005
filter = BloomFilter(number_of_elements, desired_error)

# add items to the filter
filter.add("some element")
filter.add("another")

# returns True if might be in filter, False otherwise
# note: the bloom filter can return false positives, but not false negatives
filter.maybe_element("some element")
filter.maybe_element("something")
```

## Uses
The bloom filter can be used to check if a given password is in a set of breached passwords (can be obtained from <https://haveibeenpwned.com/>).
