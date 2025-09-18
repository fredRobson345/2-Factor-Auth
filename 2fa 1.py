import random
x = 0
username = "example123"
password = "password123"

def generate_2fa_code():
    x = random.randint(0, 9999)
    return x
code = generate_2fa_code()

def main():
    user_input_username = input("Please enter your username: ")
    user_input_password = input("Please enter your password: ")
    while user_input_username != username or user_input_password != password:
        print("Incorrect username or password.")
    print(f"Your 2FA code is: {code}")
    user_input_code = int(input("Please enter the 2FA code: "))
    if user_input_code == code:
        print("Login successful!")
    else:
        print("Incorrect 2FA code. Login failed.")
       

if __name__ == "__main__":
    main()
