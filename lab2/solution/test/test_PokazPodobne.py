import os
from subprocess import Popen, PIPE
from unittest import TestCase, skipIf

FILE_NAME = "PokazPodobne.exe"
compiled = os.path.isfile(FILE_NAME)
msg = f"You need to compile {FILE_NAME} before running the tests."


@skipIf(not compiled, msg)
class TestKodPowrotu(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.COMMAND = "PokazPodobne.exe"

    def test_display_variable(self):
        variable = "TEST_VARIABLE=asdf"
        split_variable = variable.split("=")

        to_run = f"SET {variable} && {self.COMMAND} {split_variable[0]}"
        output = Popen(to_run, shell=True, stdout=PIPE).communicate()[0].decode()
        output = output.replace("\r", "")

        correct_output = f"{split_variable[0]}\n=\n{split_variable[1]}"
        self.assertIn(correct_output, output)

    def test_display_none_message(self):
        variable = "TEST_VARIABLE"

        to_run = f"{self.COMMAND} {variable}"
        output = Popen(to_run, stdout=PIPE).communicate()[0].decode()
        output = output.replace("\r", "")

        correct_output = f"{variable} = NONE"
        self.assertIn(correct_output, output)

    def test_silent_switch(self):
        variable = "TEST_VARIABLE"

        to_run = f"{self.COMMAND} {variable} /S"
        output = Popen(to_run, stdout=PIPE).communicate()[0].decode()
        output = output.replace("\r", "")

        not_silent_output = f"{variable} = NONE"
        self.assertNotIn(not_silent_output, output)

    def test_case_sensitivity(self):
        variable = "TEST_VARIABLE=asdf"
        split_variable = variable.split("=")
        lower_name = split_variable[0].lower()

        to_run = f"SET {variable} && {self.COMMAND} {lower_name}"
        output = Popen(to_run, shell=True, stdout=PIPE).communicate()[0].decode()
        output = output.replace("\r", "")

        self.assertNotIn(split_variable[0], output)
