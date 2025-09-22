import smtplib
import os
import random
import tkinter as tk
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Demo app credentials (GUI login)
APP_USERNAME = "example123"
APP_PASSWORD = "password123"

# Email Configuration (from env)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(recipient_email, subject, body, sender_email=None, sender_password=None) -> bool:
    """
    Sends an email using SMTP. Returns True on success, False on failure or dry-run.
    Uses configured EMAIL_ADDRESS/EMAIL_PASSWORD when sender not provided.
    """
    sender = sender_email or EMAIL_ADDRESS
    password = sender_password or EMAIL_PASSWORD

    if not sender or not password:
        # dry-run
        print("(Dry-run) Email contents:")
        print(f"From: {sender}")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print(body)
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, password)
            server.sendmail(sender, recipient_email, msg.as_string())

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def generate_2fa_code(length: int = 4) -> str:
    """Generate a zero-padded numeric 2FA code as a string."""
    return f"{random.randint(0, 10**length - 1):0{length}d}"

def open_2fa_dialog(root, expected_code: str):
    """Open modal 2FA dialog and verify code input."""
    def verify():
        entered = entry.get().strip()
        if entered == expected_code:
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

def on_submit(root, user_entry, pass_entry):
    user = user_entry.get().strip()
    pwd = pass_entry.get().strip()

    if user != APP_USERNAME or pwd != APP_PASSWORD:
        messagebox.showerror("Error", "Incorrect username or password.")
        return

    # credentials correct: generate code and send email to fixed recipient
    code = generate_2fa_code()
    recipient = "" ### !!!INSERT EMAIL FOR USER!!! ###
    subject = "Your 2FA Code"
    body = f"Your 2FA code is: {code}"

    sent = send_email(recipient, subject, body)
    if sent:
        messagebox.showinfo("2FA Sent", f"2FA code sent to {recipient}.")
    else:
        messagebox.showwarning("2FA Not Sent", "Email not sent. 2FA code printed to terminal for testing.")
        print(f"2FA code: {code}")

    open_2fa_dialog(root, code)

def main():
    root = tk.Tk()
    root.title("2FA Login")

    tk.Label(root, text="Username:").grid(row=0, column=0, padx=8, pady=8)
    user_entry = tk.Entry(root)
    user_entry.grid(row=0, column=1, padx=8, pady=8)

    tk.Label(root, text="Password:").grid(row=1, column=0, padx=8, pady=8)
    pass_entry = tk.Entry(root, show="*")
    pass_entry.grid(row=1, column=1, padx=8, pady=8)

    tk.Button(root, text="Submit", command=lambda: on_submit(root, user_entry, pass_entry)).grid(row=2, columnspan=2, pady=12)

    root.mainloop()

if __name__ == "__main__":
    main()


