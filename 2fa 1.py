import random
import tkinter as tk
from tkinter import messagebox
x = 0
username = "example123"
password = "password123"    
def generate_2fa_code():
    x = random.randint(0, 9999)
    return x
code = generate_2fa_code()
def main():
    def submit():
        user_input_username = entry_username.get()
        user_input_password = entry_password.get()
        # First verify username and password
        if user_input_username != username or user_input_password != password:
            messagebox.showerror("Error", "Incorrect username or password.")
            return

        # If credentials correct, open separate 2FA window
        open_2fa_window()
    
    root = tk.Tk()
    root.title("2FA Login")
    
    tk.Label(root, text="Username:").grid(row=0, column=0)
    entry_username = tk.Entry(root)
    entry_username.grid(row=0, column=1)
    
    tk.Label(root, text="Password:").grid(row=1, column=0)
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1)
    
    # 2FA entry removed from main window. It will appear in a separate dialog
    tk.Button(root, text="Submit", command=submit).grid(row=2, columnspan=2)

    # Function to open a separate Toplevel window for 2FA
    def open_2fa_window():
        def verify_2fa():
            user_input_code = entry_code.get()
            try:
                if int(user_input_code) == code:
                    messagebox.showinfo("Success", "Login successful!")
                    twofa_win.destroy()
                else:
                    messagebox.showerror("Error", "Incorrect 2FA code. Login failed.")
            except ValueError:
                messagebox.showerror("Error", "2FA code must be a number.")

        twofa_win = tk.Toplevel(root)
        twofa_win.title("Enter 2FA Code")
        twofa_win.grab_set()  # make it modal

        tk.Label(twofa_win, text="2FA Code:").grid(row=0, column=0)
        entry_code = tk.Entry(twofa_win)
        entry_code.grid(row=0, column=1)

        tk.Button(twofa_win, text="Verify", command=verify_2fa).grid(row=1, columnspan=2)
    
    print(f"Your 2FA code is: {code}")  # Output the code in the terminal
    
    root.mainloop()
if __name__ == "__main__":
    main()
