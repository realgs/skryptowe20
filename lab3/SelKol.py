import sys

COLUMN_SEPARATOR = '\t'
WRONG_ARGS_MESSAGE = 'Wrong arguments!!!'


def check_and_parse_arguments(program_args):
    try:
        selected_columns = [int(program_args[index]) for index in range(1, len(sys.argv))]
        for column_nr in selected_columns:
            if column_nr < 1 or column_nr > 4:
                print(WRONG_ARGS_MESSAGE)
                exit(1)
        return selected_columns
    except Exception:
        print(WRONG_ARGS_MESSAGE)
        exit(1)


def process_input_lines(columns_to_display):
    while True:
        try:
            product_line = input()
            product_elements = product_line.split(COLUMN_SEPARATOR)
            line = ''
            for column_nr in columns_to_display:
                line = line + product_elements[column_nr - 1] + COLUMN_SEPARATOR
            print(line)
        except Exception:
            break


selected_columns = check_and_parse_arguments(sys.argv)
process_input_lines(selected_columns)
