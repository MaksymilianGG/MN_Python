def validate_number(value, min_val=0):
    try:
        num = float(value)
        return num >= min_val
    except ValueError:
        return False

def validate_string(value):
    return bool(value.strip())

def format_currency(value):
    try:
        return f"{float(value):.2f} грн"
    except ValueError:
        return "0.00 грн"