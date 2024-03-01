def is_positive_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False

    return number > 0
