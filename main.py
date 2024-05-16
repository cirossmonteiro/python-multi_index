import unittest

class ValidatorSize:
    def __init__(self, size):
        if type(size) != list:
            raise TypeError("Size must be of list type.")
        
        if len(size) == 0:
            raise IndexError("Size cannot be a empty list.")
        
        for index in size:
            if type(index) == int:
                if index <= 0:
                    raise ValueError("Size must have only positive numbers.")
            else:
                raise TypeError("Size must have only integer numbers.")
            
        self.size = size

class MultiIndexIterator(ValidatorSize):
    def __init__(self, size):
        super().__init__(size)
        self.current = [0 for i in size]
        self.done = False

    def __iter__(self):
        return self
    
    def is_last_one(self):
        for index in range(len(self.size)-1, -1, -1):
            if self.current[index] != self.size[index]-1:
                return False
        return True
 
    def __next__(self):
        if self.done:
            raise StopIteration
        elif self.is_last_one():
            self.done = True
            return self.current
        else:
            current = self.current[:]
            
            index = len(self.current)-1
            while True:
                if self.current[index] == self.size[index]-1:
                    self.current[index] = 0
                    index -= 1
                else:
                    self.current[index] += 1
                    break

            return current

class MultiIndex(ValidatorSize):
    def __init__(self, size):
        super().__init__(size)

    def __call__(self, value):
        if type(value) == list:
            s, p = 0, 1
            for index in range(len(self.size)-1, -1, -1):
                s += p * value[index]
                p *= self.size[index]
            return s

    def __iter__(self):
        return MultiIndexIterator(self.size)
        

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.instance = MultiIndex([2,3,4])

    def test_init(self):
        with self.assertRaises(TypeError):
            MultiIndex(1)

        with self.assertRaises(IndexError):
            MultiIndex([])
        
        with self.assertRaises(ValueError):
            MultiIndex([0,1,2,3,4])

        with self.assertRaises(TypeError):
            MultiIndex([1.5,2,3,4,5])

    def test_next(self):
        all_indexes = [i for i in self.instance]
        self.assertListEqual(all_indexes[0], [0,0,0])
        self.assertListEqual(all_indexes[1], [0,0,1])
        self.assertListEqual(all_indexes[4], [0,1,0])
        self.assertListEqual(all_indexes[8], [0,2,0])
        self.assertListEqual(all_indexes[12], [1,0,0])
        self.assertListEqual(all_indexes[-1], [1,2,3])

    def test_call(self):
        self.assertEqual(0, self.instance([0,0,0]))
        self.assertEqual(1, self.instance([0,0,1]))
        self.assertEqual(4, self.instance([0,1,0]))
        self.assertEqual(8, self.instance([0,2,0]))
        self.assertEqual(12, self.instance([1,0,0]))
        self.assertEqual(23, self.instance([1,2,3]))

if __name__ == '__main__':
    unittest.main()