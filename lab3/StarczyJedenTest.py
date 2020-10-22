import subprocess
import unittest

input_data = b"10.12.2020\tKomputer1\t2532.0\t4550.50\n05.02.2020\tKomputer2\t5532.0\t14550.50"


class StarczyJedenTest(unittest.TestCase):

    def test_filter_first_row(self):
        child_process = subprocess.Popen(["python3", "StarczyJeden.py", "Komputer2"], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
        child_process.stdin.write(input_data)
        child_process_output = child_process.communicate()
        child_process.stdin.close()
        output = child_process_output[0].decode("utf-8")
        self.assertEqual("05.02.2020\tKomputer2\t5532.0\t14550.50\n", output)

    def test_show_both(self):
        expected_output = input_data.decode("utf-8") + '\n'
        child_process = subprocess.Popen(["python3", "StarczyJeden.py", "Komputer1", "Komputer2"],
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
        child_process.stdin.write(input_data)
        child_process_output = child_process.communicate()
        child_process.stdin.close()
        output = child_process_output[0].decode("utf-8")
        self.assertEqual(expected_output, output)
