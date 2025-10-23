import random

# Function to generate a random 2FA code of specified length
def generate_2fa_code(length: int = 4) -> str:
    return f"{random.randint(0, 10**length - 1):0{length}d}"