import collections
import subprocess
import pytest
import os

EXIT_CODE_EXE_PATH = os.path.join(os.path.dirname(__file__), "KodPowrotu.exe")
SHOW_ALL_EXE_PATH = os.path.join(
    os.path.dirname(__file__), "PokazWszystkie.exe")
SHOW_ALL_SIMILIAR_EXE_PATH = os.path.join(
    os.path.dirname(__file__), "PokazPodobne.exe")
CMD_SCRIPT_PATH = os.path.join(
    os.path.dirname(__file__), "skrypt_zad_4.cmd")

TEST_CASES_EXIT_CODES = [
    # NO /S
    [
        [], 11
    ],
    [
        ["0"], 0
    ],
    [
        ["9"], 9
    ],
    [
        ["a"], 12
    ],
    # /S at second position
    pytest.param([["", "/S"], 11], marks=pytest.mark.xfail),
    [
        ["0", "/S"], 0
    ],
    [
        ["9", "/s"], 9
    ],
    [
        ["a", "/S"], 12
    ],
    [
        ["B", "/s"], 12
    ],
    # /S at first position
    [
        ["/S", "0"], 0
    ],
    [
        ["/s", "9"], 9
    ],
    [
        ["/S", "z"], 12
    ],
    [
        ["/s", "C"], 12
    ],
    # more than one arg without /S
    [
        ["1", "2"], 13
    ],
    [
        ["3", "a"], 13
    ],
    [
        ["a", "4"], 13
    ],
    [
        ["b", "a"], 13
    ],
    # more than two args with /S
    [
        ["1", "2", "/S"], 13
    ],
    [
        ["3", "/S", "a"], 13
    ],
    [
        ["/S", "a", "4"], 13
    ],
    [
        ["b", "a", "/s"], 13
    ],
    [
        ["6", "/s", "A"], 13
    ],
    [
        ["/s", "D", "6"], 13
    ],
]

TEST_CASES_EXIT_CODES_IDS = [
    "empty",
    "0",
    "9",
    "a",
    "/S",
    "0 /S",
    "9 /s",
    "a /S",
    "B /s",
    "/S 0",
    "/s 9",
    "/S z",
    "/s C",
    "1 2",
    "3 a",
    "a 4",
    "b a",
    "1 2 /S",
    "3 /S a",
    "/S a 4",
    "b a /s",
    "6 /s A",
    "/s D 6",
]

TEST_CASES_SHOW_ALL = [
    [],
    ["1"],
    ["a", "2"],
    ["/S", "4"]
]

TEST_CASES_SHOW_ALL_IDS = ["empty", "1", "a 2", "/S 4"]

TEST_CASES_SHOW_SIMILIAR = [
    # Standard
    [],
    ["/S"],
    ["/s"],
    ["xd"],
    ["OS"],
    # /S on diff positions, only single NONE outputs
    ["xd", "/S"],
    ["xd", "/s"],
    ["xd", "/S", "xd"],
    ["xd", "/s", "xd"],
    ["/S", "xd", "xd"],
    ["/s", "xd", "xd"],
    ["xd", "xd", "/S"],
    ["xd", "xd", "/s"],
    # /S on diff positions, only single OS outputs
    ["OS", "/S"],
    ["OS", "/s"],
    ["OS", "/S", "OS"],
    ["OS", "/s", "OS"],
    ["/S", "OS", "OS"],
    ["/s", "OS", "OS"],
    ["OS", "OS", "/S"],
    ["OS", "OS", "/s"],
    # single OS outputs and NONE outputs
    ["OS", "xd"],
    ["xd", "OS"],
    ["OS", "xd", "OS"],
    ["xd", "xd", "OS", "OS"],
    ["OS", "xd", "xd" "OS"],
    ["xd", "OS", "xd", "OS"],
    ["xd", "OS", "OS", "xd"],
    ["OS", "xd", "OS", "xd"],
    ["OS", "OS", "xd", "xd"],
    # single OS outputs and silenced (/S) NONE outputs
    ["OS", "xd", "/S"],
    ["/s", "xd", "OS"],
    ["OS", "/s", "xd", "OS"],
    ["xd", "xd", "/s", "OS", "OS"],
    ["OS", "xd", "xd", "/s", "OS"],
    ["xd", "/S", "OS", "xd", "OS"],
    ["xd", "OS", "/S", "OS", "xd"],
    ["OS", "xd", "OS", "/S", "xd"],
    ["/S", "OS", "OS", "xd", "xd"],
    # many outputs: OS, Path, ProgramData
    ["OS", "Path", "ProgramData"],
    ["OS", "Path", "XD", "Path", "ProgramData"],
    ["OS", "Path", "ProgramData"],
    ["OS",  "Path", "Path", "XD", "ProgramData"],
    ["Path", "OS", "Path", "ProgramData"],
    ["OS", "Path", "ProgramData" "Path", "XD"],
]

TEST_CASES_SHOW_SIMILIAR_IDS = [" ".join(x) for x in TEST_CASES_SHOW_SIMILIAR]

TEST_CASES_CMD_SCRIPT = [
    [[], "Brak parametrow"],
    [["0"], "Przekazano: 0"],
    [["9"], "Przekazano: 9"],
    [["a"], "Parametr a nie jest cyfra"],
    [["1", "2"], "Niewlasciwa wartosc parametru 1 2"],
    [["b", "3"], "Niewlasciwa wartosc parametru b 3"],
    [["5", "z", "3"], "Niewlasciwa wartosc parametru 5 z 3"]
]

TEST_CASES_CMD_SCRIPT_IDS = ["".join(x[1]) for x in TEST_CASES_CMD_SCRIPT]


@pytest.mark.parametrize("current_testcase", TEST_CASES_EXIT_CODES, ids=TEST_CASES_EXIT_CODES_IDS)
def test_exit_codes(current_testcase):
    # Init params
    params, expected_exit_code = current_testcase

    # Run Exit Code .exe file
    process = subprocess.Popen(
        [EXIT_CODE_EXE_PATH] + params, stdout=subprocess.PIPE, shell=False)

    # Get exit code and stdoutput
    actual_stdoutput = process.stdout.read().strip().decode("utf-8")
    actual_exit_code = process.wait()

    # Compare exit codes
    assert actual_exit_code == expected_exit_code

    # Check std output
    if "/S" in params or "/s" in params:
        assert "" == actual_stdoutput
    else:
        assert str(expected_exit_code) == actual_stdoutput


@pytest.mark.parametrize("current_testcase", TEST_CASES_SHOW_ALL, ids=TEST_CASES_SHOW_ALL_IDS)
def test_show_all(current_testcase):
    # Run Show All .exe file and get stdoutput as lines
    process = subprocess.Popen(
        [SHOW_ALL_EXE_PATH] + current_testcase, stdout=subprocess.PIPE, shell=False)
    actual_stdoutput = [x.decode('latin-1').rstrip('\n').rstrip('\r')
                        for x in iter(process.stdout.readlines())]

    # Check whether most important env vars were printed
    assert search_for_word("TEMP", actual_stdoutput)
    assert search_for_word("PATH", actual_stdoutput)
    assert search_for_word("OS", actual_stdoutput)
    assert search_for_word("APPDATA", actual_stdoutput)
    assert search_for_word(os.path.basename(__file__), actual_stdoutput)

    # Check whether program's params were printed (at the end of stdoutput)
    params_len = len(current_testcase)
    for i, param in enumerate(current_testcase):
        assert param == actual_stdoutput[-params_len+i]


@pytest.mark.parametrize("current_testcase", TEST_CASES_SHOW_SIMILIAR, ids=TEST_CASES_SHOW_SIMILIAR_IDS)
def test_show_similiar(current_testcase):
    # Run Show Similiar .exe path and get stdoutput as lines
    process = subprocess.Popen(
        [SHOW_ALL_SIMILIAR_EXE_PATH] + current_testcase, stdout=subprocess.PIPE, shell=False)
    actual_stdoutput = [x.decode('latin-1').rstrip('\n').rstrip('\r').rstrip('')
                        for x in iter(process.stdout.readlines())]
    actual_stdoutput = [x for x in actual_stdoutput if x != ""]

    # Get actual counter
    actual_counter = collections.Counter("".join(actual_stdoutput))

    # Get expected countert
    expected_stdoutput = show_similiar_ref(current_testcase).replace("\n", "")
    expected_counter = collections.Counter("".join(expected_stdoutput))

    assert expected_counter == actual_counter


@pytest.mark.parametrize("current_testcase", TEST_CASES_CMD_SCRIPT, ids=TEST_CASES_CMD_SCRIPT_IDS)
def test_cmd_script(current_testcase):
    # Init params
    params, expected_stdoutput = current_testcase

    # Run Cmd Script and get stdoutput
    process = subprocess.Popen(
        [CMD_SCRIPT_PATH] + params, stdout=subprocess.PIPE, shell=False)
    actual_stdoutput = process.stdout.read().strip().decode("utf-8")

    # Check stdoutput
    assert expected_stdoutput == actual_stdoutput


# UTILS - returns bool if given world is somewhere inside given list
def search_for_word(the_word, list_of_lines):
    for single_line in list_of_lines:
        if the_word in single_line:
            return True
    return False


# UTILS - This is reference PokazPodobne.exe method - but in python
def show_similiar_ref(params):
    process = subprocess.Popen([SHOW_ALL_EXE_PATH], stdout=subprocess.PIPE, shell=False)
    actual_stdoutput = [x.decode('latin-1').rstrip('\n').rstrip('\r')
                        for x in iter(process.stdout.readlines())]
    envs_dict = {}
    for line in actual_stdoutput[:-1]:
        env_name, env_cont = line.split("=")
        envs_dict[env_name] = env_cont.split(";")
    stdoutput = ""
    unique_params = set(params)
    not_used_params = unique_params.copy()
    for param in unique_params:
        for key, value in envs_dict.items():
            if param in key:
                stdoutput += "\n"+key+"\n=\n"+"\n".join(value)
                if param in not_used_params:
                    not_used_params.remove(param)

    if "/S" not in unique_params and "/s" not in unique_params:
        for param in not_used_params:
            stdoutput += "\n"+param + " = NONE"
    return stdoutput
 