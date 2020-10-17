import os
from subprocess import Popen, DEVNULL, PIPE
from unittest import TestCase, skipIf

FILE_NAME = "KodPowrotu.exe"
compiled = os.path.isfile(FILE_NAME)
msg = f"You need to compile {FILE_NAME} before running the tests."


@skipIf(not compiled, msg)
class TestKodPowrotu(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.COMMAND = "KodPowrotu.exe"

    def test_return_correct_digit(self):
        args = [x for x in range(10)]
        for arg in args:
            with self.subTest(arg=arg):
                return_value = Popen(f"{self.COMMAND} {arg}", stdout=DEVNULL).wait()
                self.assertEqual(arg, return_value)

    def test_not_enough_parameters(self):
        args = ["", "/s", "/s /f"]
        for arg in args:
            with self.subTest(arg=arg):
                return_value = Popen(f"{self.COMMAND} {arg}", stdout=DEVNULL).wait()
                self.assertEqual(11, return_value)

    def test_not_a_digit(self):
        args = ["asd", "123", "1asd", "-5", "4.5"]
        for arg in args:
            with self.subTest(arg=arg):
                return_value = Popen(f"{self.COMMAND} {arg}", stdout=DEVNULL).wait()
                self.assertEqual(12, return_value)

    def test_too_many_parameters(self):
        args = ["1 2", "asd 1", "-4 5", "1 3 /s /f"]
        for arg in args:
            with self.subTest(arg=arg):
                return_value = Popen(f"{self.COMMAND} {arg}", stdout=DEVNULL).wait()
                self.assertEqual(13, return_value)

    def test_silent_switch(self):
        args = ["1 /s", "1 /S", "/s 1", "/S 1", "asd /s", "/S", "1 1 1 /S", "/s /f"]
        for arg in args:
            with self.subTest(arg=arg):
                output = Popen(f"{self.COMMAND} {arg}", stdout=PIPE).communicate()[0]
                self.assertEqual("", output.decode())
