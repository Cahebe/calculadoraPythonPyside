def is_valid_number(string: str):
    """Verifica se o numero é valido"""
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid


def is_empty(string: str):
    return len(string) == 0


def is_num_or_dot(char: str) -> bool:
    """Retorna True se for um dígito (0-9) ou um ponto."""
    return char.isdigit() or char == '.'
