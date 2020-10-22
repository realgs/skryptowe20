import sys

COLUMN_SEPARATOR = '\t'


def check_if_set_contains_at_least_one_element(elements, value_set):
    for element in elements:
        if element in value_set:
            return True
    return False


product_params = set(sys.argv)
if len(product_params) > 0:
    while True:
        try:
            product_line = input()
            product_elements = product_line.split(COLUMN_SEPARATOR)
            if check_if_set_contains_at_least_one_element(product_elements, product_params):
                print(product_line)
        except Exception:
            break
