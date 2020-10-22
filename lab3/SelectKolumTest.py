import subprocess
import unittest

input_data = b"10.12.2020\tKomputer1\t2532.0\t4550.50\n05.02.2020\tKomputer2\t5532.0\t14550.50"


class SelectKolumTest(unittest.TestCase):

    def test_show_first_column_only(self):
        child_process = subprocess.Popen(["python3", "SelKol.py", "1"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        child_process.stdin.write(input_data)
        child_process_output = child_process.communicate()
        child_process.stdin.close()
        output = child_process_output[0].decode("utf-8")
        self.assertEqual("10.12.2020\t\n05.02.2020\t\n", output)

    def test_show_first_third_and_fourth_column(self):
        child_process = subprocess.Popen(["python3", "SelKol.py", "3", "4"], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
        child_process.stdin.write(input_data)
        child_process_output = child_process.communicate()
        child_process.stdin.close()
        output = child_process_output[0].decode("utf-8")
        self.assertEqual("2532.0\t4550.50\t\n5532.0\t14550.50\t\n", output)
