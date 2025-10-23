# Authentication module using predefined credentials
APP_USERNAME = "example123"
APP_PASSWORD = "password123"

# Function to verify username and password
def verify_credentials(username: str, password: str) -> bool:
    return username == APP_USERNAME and password == APP_PASSWORD