import unittest
from SortingMethods import bubbleSort, quickSort


class SortingMethodsTestCase(unittest.TestCase):
    def testBubbleCorrect(self):
        testList = [0, -20, 3, 526, -464, -65, 235, 6, 66, -4]
        self.assertTrue(bubbleSort(testList))
        self.assertEqual(testList, [-464, -65, -20, -4, 0, 3, 6, 66, 235, 526])

    def testBubbleEmpty(self):
        testList = []
        self.assertTrue(bubbleSort(testList))
        self.assertEqual(testList, [])

    def testBubbleOneElement(self):
        testList = [1]
        self.assertTrue(bubbleSort(testList))
        self.assertEqual(testList, [1])

    
if __name__ == '__main__':
    unittest.main()
