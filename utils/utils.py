def bool_from_str(text: str) -> bool:
    if text.lower() == 'true':
        return True
    elif text.lower() == 'false':
        return False
