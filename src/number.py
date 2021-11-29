def is_nan(string):
    return string != string


def format_value(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if is_nan(element):
        return 0.0
    if type(element) == str:
        element = element.replace('R$', '').replace('.', '').replace(',', '.').replace(' ', '').replace('"','').replace("'",'')

    return float(element)
    