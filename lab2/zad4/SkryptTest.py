import subprocess
import unittest


class SkryptCase(unittest.TestCase):
    def setUp(self):
        subprocess.run(['g++', 'KodPowrotu.cpp', '-o', 'KodPowrotu'])

    def test_proper_number(self):
        result = subprocess.run(['./Skrypt.sh', '55'], stdout=subprocess.PIPE)
        self.assertTrue('Przekazano: prawidłowa wartość' in result.stdout.decode())

    def test_wrong_number(self):
        result = subprocess.run(['./Skrypt.sh', 'adsdas'], stdout=subprocess.PIPE)
        self.assertTrue('Parametr adsdas nie jest cyfrą' in result.stdout.decode())
