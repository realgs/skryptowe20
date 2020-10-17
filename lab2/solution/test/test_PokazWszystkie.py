import os
from subprocess import Popen, PIPE
from unittest import TestCase, skipIf

FILE_NAME = "PokazWszystkie.exe"
compiled = os.path.isfile(FILE_NAME)
msg = f"You need to compile {FILE_NAME} before running the tests."


@skipIf(not compiled, msg)
class TestKodPowrotu(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.COMMAND = "PokazWszystkie.exe"

    def test_display_environmental_variable(self):
        variable = "TEST_VARIABLE=asdf"
        to_run = f"SET {variable} && {self.COMMAND}"
        output = Popen(to_run, shell=True, stdout=PIPE).communicate()[0].decode()
        self.assertIn(variable, output)

    def test_display_parameter(self):
        parameter = "parameter_that_is_unlikely_to_already_be_in_the_output"
        non_parameter = "/switchthatisunlikelytobeintheoutput"
        to_run = f"{self.COMMAND} {parameter} {non_parameter}"
        output = Popen(to_run, shell=True, stdout=PIPE).communicate()[0].decode()
        self.assertIn(parameter, output)
        self.assertNotIn(non_parameter, output)
