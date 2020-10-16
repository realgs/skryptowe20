import subprocess
import unittest


class KodPowrotuCase(unittest.TestCase):
    def setUp(self):
        subprocess.run(['g++', 'KodPowrotu.cpp', '-o', 'KodPowrotu'])

    def test_proper_number(self):
        result = subprocess.run(['./KodPowrotu', '65'], stdout=subprocess.PIPE)
        self.assertTrue('65' in result.stdout.decode())
        self.assertEqual(65, result.returncode)

    def test_proper_number2(self):
        result = subprocess.run(['./KodPowrotu', '-65'], stdout=subprocess.PIPE)
        self.assertTrue('65' in result.stdout.decode())
        self.assertEqual(191, result.returncode, )

    def test_proper_number_silent(self):
        result = subprocess.run(['./KodPowrotu', '65', '/S'], stdout=subprocess.PIPE)
        self.assertEqual(65, result.returncode)

    def test_no_arguments(self):
        result = subprocess.run(['./KodPowrotu'], stdout=subprocess.PIPE)
        self.assertTrue('11' in result.stdout.decode())
        self.assertEqual(11, result.returncode)

    def test_no_arguments_silent(self):
        result = subprocess.run(['./KodPowrotu'], stdout=subprocess.PIPE)
        self.assertEqual(11, result.returncode)

    def test_argument_is_not_a_number(self):
        result = subprocess.run(['./KodPowrotu', 'adssad'], stdout=subprocess.PIPE)
        self.assertTrue('12' in result.stdout.decode())
        self.assertEqual(12, result.returncode, )

    def test_argument_is_not_a_number_silent(self):
        result = subprocess.run(['./KodPowrotu', 'adssad'], stdout=subprocess.PIPE)
        self.assertEqual(12, result.returncode)
