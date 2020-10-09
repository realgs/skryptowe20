import unittest
from SortingMethods import bubbleSort, quickSort


class BubbleSortTestCase(unittest.TestCase):
    def testBubbleCorrect(self):
        testList = [0, -20.52, 3, 526, -464.5, -65, 235, 6, 66.947, -4]
        self.assertTrue(bubbleSort(testList))
        self.assertEqual(testList, [-464.5, -65, -20.52, -4, 0, 3, 6, 66.947, 235, 526])

    def testBubbleEmpty(self):
        testList = []
        self.assertTrue(bubbleSort(testList))
        self.assertEqual(testList, [])

    def testBubbleOneElement(self):
        testList = [1]
        self.assertTrue(bubbleSort(testList))
        self.assertEqual(testList, [1])

    def testBubbleNotNumericElementsInList(self):
        testList = [1, "adfa", 523, False, [2, 4, 5], 3]
        self.assertFalse(bubbleSort(testList))

        testList = [True, [12], 2]
        self.assertFalse(bubbleSort(testList))

        testList = [[52], 2, "sadf"]
        self.assertFalse(bubbleSort(testList))


class QuickSortTestCase(unittest.TestCase):
    def testQuickCorrect(self):
        testList = [0, -20.52, 3, 526, -464.5, -65, 235, 6, 66.947, -4]
        self.assertTrue(quickSort(testList))
        self.assertEqual(testList, [-464.5, -65, -20.52, -4, 0, 3, 6, 66.947, 235, 526])

    def testQuickEmpty(self):
        testList = []
        self.assertTrue(quickSort(testList))
        self.assertEqual(testList, [])

    def testQuickOneElement(self):
        testList = [1]
        self.assertTrue(quickSort(testList))
        self.assertEqual(testList, [1])

    def testQuickNotNumericElementsInList(self):
        testList = [1, "adfa", 523, False, [2, 4, 5], 3]
        self.assertFalse(quickSort(testList))

        testList = [True, [12], 2]
        self.assertFalse(quickSort(testList))

        testList = [[52], 2, "sadf"]
        self.assertFalse(quickSort(testList))


if __name__ == '__main__':
    unittest.main()
