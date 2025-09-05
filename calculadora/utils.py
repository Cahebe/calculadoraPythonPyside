def is_valid_number(string: str):
    """Verifica se o numero é valido"""
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid
