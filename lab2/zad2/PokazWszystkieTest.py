import subprocess
import unittest


class PokazWszystkieTestCase(unittest.TestCase):
    def setUp(self):
        subprocess.run(['g++', 'PokazWszystkie.cpp', '-o', 'PokazWszystkie'])

    def test_displayed_data(self):
        env_result = subprocess.run(['printenv'], stdout=subprocess.PIPE)
        proper_envs = list(filter(lambda variable: len(variable) > 3, env_result.stdout.decode().split("\n")))
        result = subprocess.run(['./PokazWszystkie', 'arg1', 'arg2'], stdout=subprocess.PIPE)
        displayed_data = result.stdout.decode()
        self.assertTrue('arg1' in displayed_data)
        self.assertTrue('arg2' in displayed_data)
        for env in proper_envs:
            self.assertTrue(env in displayed_data)
