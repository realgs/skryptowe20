# ------------------------------- Imports --------------------------------------


import pytest
import random
from random_sort import random_sort
from quick_sort import quick_sort


# ----------------------------- Test Cases -------------------------------------


# SORTING FUNCTIONS
SORTING_FUNCTIONS = [
    pytest.param(random_sort, id="Random Sort", marks=pytest.mark.skip),
    pytest.param(quick_sort, id="Quick Sort"),
]


# INTEGERS
ONLY_INTEGERS = [
    [
        0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
    ],
    [
        89, 55, 34, 21, 13, 8, 5, 3, 2, 1, 0
    ],
    [
        13, 1, 55, 89, 3, 2, 0, 5, 21, 8, 34
    ],
    [
        5, 0, 5, 1, 8, 3, 3, 13, 34, 1, 2, 89, 55, 0, 55, 89, 89, 3, 5, 2, 8, 21
    ],
    [
        -89, -55, -34, -21, -13, -8, -5, -3, -2, -1
    ],
    [
        -1, -2, -3, -5, -8, -13, -21, -34, -55, -89
    ],
    [
        -13, -1, -55, -89, -3, -2, -5, -21, -8, -34
    ],
    [
        -1, -5, -5, -1, -8, -3, -3, -2, -89, -55, -55, -89, -89, -3, -2, -2, -21
    ],
    [
        -8, -5, -3, -2, -1, 1, 2, 3, 5, 8
    ],
    [
        8, 5, 3, 2, 1, -1, -2, -3, -5, -8
    ],
    [
        -13, 1, -55, -89, 3, 2, -5, 21, -8, -34
    ],
    [
        -1, 5, -5, -1, 8, 3, 3, -13, 34, -1, 2, -89, 55, 55, -89, 3, -5, 2, -8, 21
    ],
]


# STRINGS
ONLY_INTEGERS_IDS = [
    "Integers: positive, sorted",
    "Integers: positive, vice versa",
    "Integers: positive, random",
    "Integers: positive, random, with repeats",
    "Integers: negative, sorted",
    "Integers: negative, vice versa",
    "Integers: negative, random",
    "Integers: negative, random, with repeats",
    "Integers: positive and negative, sorted",
    "Integers: positive and negative, vice versa",
    "Integers: positive and negative, random",
    "Integers: positive and negative, random, with repeats",
]

ONLY_STRINGS = [
    [
        "a", "b", "c", "d", "e", "f", "g", "u", "v", "z"
    ],
    [
        "z", "v", "u", "g", "f", "e", "d", "c", "b", "a"
    ],
    [
        "a", "s", "u", "w", "j", "f", "y", "b", "t" "r"
    ],
    [
        "a", "a", "f", "a", "f", "s", "f", "u", "w",
        "j", "f", "u", "y", "b", "t", "a", "r"
    ],
    [
        "Lorem", "Ut", "Vivamus", "adipiscing", "amet", "congue", "consectetur",
        "dolor", "elit", "et", "ex", "felis", "ipsum", "lacinia", "mollis",
        "nunc", "rhoncus", "sit", "ut", "viverra"
    ],
    [
        "viverra", "ut", "sit", "rhoncus", "nunc", "mollis", "lacinia", "ipsum",
        "felis", "ex", "et", "elit", "dolor", "consectetur", "congue", "amet",
        "adipiscing""Vivamus", "Ut", "Lorem"
    ],
    [
        "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing",
        "elit", "Vivamus", "viverra", "lacinia", "felis", "et", "congue",
        "nunc", "mollis", "rhoncus", "Ut", "ut", "ex"
    ],
    [
        "Lorem",  "Ut", "sit", "ipsum", "et", "dolor", "ipsum", "sit",  "et",
        "amet", "Ut", "consectetur", "adipiscing",  "viverra", "elit", "Vivamus",
        "viverra", "viverra", "t", "lacinia", "viverra",  "felis", "et",
        "congue", "nunc", "mollis",  "et", "rhoncus", "ex", "Ex", "ex"
    ],
]

ONLY_STRINGS_IDS = [
    "Strings: chars, sorted",
    "Strings: chars, vice versa",
    "Strings: chars, random",
    "Strings: chars, random, with repeats",
    "Strings: words, sorted",
    "Strings: words, vice versa",
    "Strings: words, random",
    "Strings: words, random, with repeats",
]


# ONE ELEMENT
ONLY_ONE_ELEMENT = [[1], ["A"], [False]]

ONLY_ONE_ELEMENT_IDS = ["One Integer", "One String", "One Boolean"]


# EMPTY LIST
EMPTY_LIST = [[]]
EMPTY_LIST_IDS = ["Empty"]


# ------------------------------- Tests ----------------------------------------


# INTEGERS
@pytest.mark.parametrize("only_integer_list", ONLY_INTEGERS, ids=ONLY_INTEGERS_IDS)
@pytest.mark.parametrize("sorting_func", SORTING_FUNCTIONS)
def test_integers(only_integer_list, sorting_func):
    """
    This test checks whether both: quick sort and random sort methods works
    as they should. Here are tested only python int values.

    **Test Inputs**

    * list of integers
    * sorting function

    **Test Procedure**

    Run sorting function with copy of current test list.
    Check whether returned list is sorted.

    **Pass/Fail Criteria**

    There should not be any exceptions.
    Returned list should have same length as original list.
    Returned list should be sorted ascending.

    **Params**

    :param only_integer_list: not empty list with only integer values
    :param sorting_func: sorting function

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    result = sorting_func(only_integer_list.copy())
    assert len(result) == len(only_integer_list)
    assert is_sorted(result)


# STRINGS
@pytest.mark.parametrize("only_string_list", ONLY_STRINGS, ids=ONLY_STRINGS_IDS)
@pytest.mark.parametrize("sorting_func", SORTING_FUNCTIONS)
def test_strings(only_string_list, sorting_func):
    """
    This test checks whether both: quick sort and random sort methods works
    as they should. Here are tested only python string values - both 
    single chars cases and full words cases.

    **Test Inputs**

    * list of strings or single chars (they are in fact also strings)
    * sorting function

    **Test Procedure**

    Run sorting function with copy of current test list.
    Check whether returned list is sorted.

    **Pass/Fail Criteria**

    There should not be any exceptions.
    Returned list should have same length as original list.
    Returned list should be sorted ascending.

    **Params**

    :param list_to_sort: not empty list with only string values
    :param sorting_func: sorting function

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    result = sorting_func(only_string_list.copy())
    assert len(result) == len(only_string_list)
    assert is_sorted(result)


# ONE ELEMENT
@pytest.mark.parametrize("one_element_list", ONLY_ONE_ELEMENT, ids=ONLY_ONE_ELEMENT_IDS)
@pytest.mark.parametrize("sorting_func", SORTING_FUNCTIONS)
def test_one_element(one_element_list, sorting_func):
    """
    This test checks how both: quick sort and random sort methods
    interpret single value list cases. Here are tested lists with: 
    integer, string and boolean.

    **Test Inputs**

    * list with only one element
    * sorting function

    **Test Procedure**

    Run sorting function with copy of current test one element list.
    Check if original list is the same as returned.

    **Pass/Fail Criteria**

    There should not be any exceptions.
    Returned list should have only one element, the same as original.

    **Params**

    :param one_element_list: one element list
    :param sorting_func: sorting function

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    result = sorting_func(one_element_list.copy())
    assert len(result) == 1
    assert result[0] == one_element_list[0]


# EMPTY LIST
@pytest.mark.parametrize("empty_list", EMPTY_LIST, ids=EMPTY_LIST_IDS)
@pytest.mark.parametrize("sorting_func", SORTING_FUNCTIONS)
def test_empty(empty_list, sorting_func):
    """
    This test checks how both: quick sort and random sort methods interpret 
    empty list. List like this cannot be sorted, so these sorting
    functions should at least not throw any exception.

    **Test Inputs**

    * empty list
    * sorting function

    **Test Procedure**

    Run sorting function with epmty list.
    Try to catch any possible exception.

    **Pass/Fail Criteria**

    There should not be any exceptions.

    **Params**

    :param list_to_sort: empty list
    :param sorting_func: sorting function

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    try:
        sorting_func(empty_list)
    except Exception as e:
        assert False, e


# --------------------------------- Utils --------------------------------------


def is_sorted(list_to_check):
    """
    This is one helpful function that checks whether given list 
    is sorted ascending and returns boolean value.

    **Params**

    :param list_to_check: list that will be investigated
    :return: result - boolean value

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    for i in range(len(list_to_check) - 1):
        if list_to_check[i] > list_to_check[i+1]:
            return False
    return True
