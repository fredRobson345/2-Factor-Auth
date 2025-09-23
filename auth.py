APP_USERNAME = "example123"
APP_PASSWORD = "password123"

def verify_credentials(username: str, password: str) -> bool:
    """
    Simple credential check. Replace with real auth as needed.
    """
    return username == APP_USERNAME and password == APP_PASSWORD