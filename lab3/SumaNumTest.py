import subprocess
import unittest


class SumaNumTest(unittest.TestCase):

    def test_sum_full_product(self):
        input_data = b"10.12.2020\tKomputer1\t20.0\t10.50\n05.02.2020\tKomputer2\t40.50\t100.51"
        child_process = subprocess.Popen(["python3", "SumaNum.py"], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
        child_process.stdin.write(input_data)
        child_process_output = child_process.communicate()
        child_process.stdin.close()
        output = child_process_output[0].decode("utf-8")
        self.assertEqual("171.51\n", output)

    def test_sum_partial_product(self):
        input_data = b"Komputer1\t420.0\nKomputer2\t40.50"
        child_process = subprocess.Popen(["python3", "SumaNum.py"], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
        child_process.stdin.write(input_data)
        child_process_output = child_process.communicate()
        child_process.stdin.close()
        output = child_process_output[0].decode("utf-8")
        self.assertEqual("460.5\n", output)
