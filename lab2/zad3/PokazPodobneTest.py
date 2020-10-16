import subprocess
import unittest
import os


class PokazPodobneTestCase(unittest.TestCase):
    def setUp(self):
        subprocess.run(['g++', 'PokazPodobne.cpp', '-o', 'PokazPodobne'])

    def test_displayed_env(self):
        os.environ['TEST_ENV1'] = 'randomValue'
        os.environ['TEST_ENV2'] = 'val1;val2'
        result = subprocess.run(['./PokazPodobne', 'val'], stdout=subprocess.PIPE)
        displayed_data = result.stdout.decode()
        self.assertTrue('TEST_ENV1 = NONE' in displayed_data)
        self.assertTrue('TEST_ENV2\n=\nval1\nval2\n' in displayed_data)

    def test_no_argument(self):
        result = subprocess.run(['./PokazPodobne'], stdout=subprocess.PIPE)
        self.assertEqual(11, result.returncode)

    def test_displayed_env_silent1(self):
        os.environ['TEST_ENV1'] = 'randomValue'
        os.environ['TEST_ENV2'] = 'val1;val2'
        result = subprocess.run(['./PokazPodobne', 'val', '/S'], stdout=subprocess.PIPE)
        displayed_data = result.stdout.decode()
        self.assertTrue('TEST_ENV1 = NONE' not in displayed_data)
        self.assertTrue('TEST_ENV2\n=\nval1\nval2\n' == displayed_data)

    def test_displayed_env_silent2(self):
        os.environ['TEST_ENV1'] = 'randomValue'
        os.environ['TEST_ENV2'] = 'val1;val2'
        result = subprocess.run(['./PokazPodobne', 'val', '/s'], stdout=subprocess.PIPE)
        displayed_data = result.stdout.decode()
        self.assertTrue('TEST_ENV1 = NONE' not in displayed_data)
        self.assertTrue('TEST_ENV2\n=\nval1\nval2\n' == displayed_data)
