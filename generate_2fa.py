import random

def generate_2fa_code(length: int = 4) -> str:
    """
    Generate a zero-padded numeric 2FA code as a string.
    """
    return f"{random.randint(0, 10**length - 1):0{length}d}"