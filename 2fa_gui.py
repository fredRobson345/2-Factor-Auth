#tKinter import to create the GUI 
import tkinter as tk
from tkinter import messagebox

#files imported with external functions 
from generate_2fa import generate_2fa_code
from emailer import send_email
from auth import verify_credentials

#recipient email for the code to be email to
RECIPIENT = "example@gmail.com" # replace with email

#2 factor authentication GUI, run when username and password are correct
def open_2fa_dialog(root, expected_code: str):
    def verify():
        if entry.get().strip() == expected_code:
            messagebox.showinfo("Success", "Login successful!")
            twofa.destroy()
            root.destroy()
        else:
            messagebox.showerror("Error", "Incorrect 2FA code.")

    twofa = tk.Toplevel(root)
    twofa.title("Enter 2FA Code")
    twofa.grab_set()
    tk.Label(twofa, text="2FA Code:").grid(row=0, column=0, padx=8, pady=8)
    entry = tk.Entry(twofa)
    entry.grid(row=0, column=1, padx=8, pady=8)
    tk.Button(twofa, text="Verify", command=verify).grid(row=1, columnspan=2, pady=(0,8))

#function that is run when the username and password are submitted
def on_submit(root, username_entry, password_entry):
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if not verify_credentials(username, password):
        messagebox.showerror("Error", "Incorrect username or password.")
        return

    
    # generates code from generate_2fa.py and sends email using emailer.py
    code = generate_2fa_code()
    subject = "Your 2FA Code"
    body = f"Your 2FA code is: {code}"
    sent = send_email(RECIPIENT, subject, body)
    if sent:
        messagebox.showinfo("2FA Sent", f"2FA code sent to {RECIPIENT}.")
    else:
        messagebox.showwarning("2FA Not Sent", "Email not sent. 2FA code printed to terminal.")
        print(f"2FA code: {code}")

    open_2fa_dialog(root, code)

def main():
    
    # creating GUI window to input the username and password 
    root = tk.Tk()
    root.title("2FA Login")
    tk.Label(root, text="Username:").grid(row=0, column=0, padx=8, pady=8)
    username_entry = tk.Entry(root); username_entry.grid(row=0, column=1, padx=8, pady=8)
    tk.Label(root, text="Password:").grid(row=1, column=0, padx=8, pady=8)
    password_entry = tk.Entry(root, show="*"); password_entry.grid(row=1, column=1, padx=8, pady=8)
    tk.Button(root, text="Submit", command=lambda: on_submit(root, username_entry, password_entry)).grid(row=2, columnspan=2, pady=12)
    root.mainloop()

if __name__ == "__main__":
    main()