import hashlib
import os
import re
import uuid
from datetime import datetime

class User:
    def __init__(self, username, email, password):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)
        self.created_at = datetime.now()

    @staticmethod
    def hash_password(password):
        salt = os.urandom(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + password_hash

    def verify_password(self, password):
        salt = self.password_hash[:32]
        stored_password_hash = self.password_hash[32:]
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return password_hash == stored_password_hash

class AuthSystem:
    def __init__(self):
        self.users = {}

    def register(self, username, email, password):
        if not self.validate_email(email):
            return "Invalid email format."

        if not self.validate_password(password):
            return "Password must contain at least 8 characters, including letters and numbers."

        if email in self.users:
            return "Email already registered."

        new_user = User(username, email, password)
        self.users[email] = new_user
        return f"User {username} registered successfully."

    def login(self, email, password):
        user = self.users.get(email)
        if not user:
            return "User not found."

        if user.verify_password(password):
            return f"Welcome back, {user.username}!"
        else:
            return "Invalid password."

    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False

        has_letter = any(char.isalpha() for char in password)
        has_number = any(char.isdigit() for char in password)

        return has_letter and has_number

if __name__ == "__main__":
    auth_system = AuthSystem()

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            print(auth_system.register(username, email, password))

        elif choice == "2":
            email = input("Enter email: ")
            password = input("Enter password: ")
            print(auth_system.login(email, password))

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")