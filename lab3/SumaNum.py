COLUMN_SEPARATOR = '\t'
result_sum = 0.0
while True:
    try:
        product_line = input()
        product_elements = product_line.split(COLUMN_SEPARATOR)
        for product_element in product_elements:
            try:
                result_sum += float(product_element)
            except Exception:
                pass
    except Exception:
        print(result_sum)
        break
