import os
from datetime import datetime

def main_menu():
    print("\nWelcome to the Main Menu!")
    print("1. User Login")
    print("2. Admin Login")
    print("3. Quit")
    selection = input("Please select an option: ")
    return selection

def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    try:
        with open("PMS/Admins.txt", "r", encoding="utf8") as file:
            for line in file:
                parts = line.strip().split("-")
                if len(parts) == 2:
                    correct_username, correct_password = parts
                    if username == correct_username and password == correct_password:
                        add_log_entry(username)
                        print(f"Welcome, admin {username}!")
                        return username
        print("Incorrect admin username or password.")
        return None
    except FileNotFoundError:
        print("Error: 'PMS/Admins.txt' file not found.")
        return None

def user_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        with open("PMS/Users.txt", "r", encoding="utf8") as file:
            for line in file:
                parts = line.strip().split("-")
                if len(parts) == 2:
                    correct_username, correct_password = parts
                    if username == correct_username and password == correct_password:
                        add_log_entry(username)
                        print(f"Welcome, {username}!")
                        return username
        print("Incorrect username or password.")
        return None
    except FileNotFoundError:
        print("Error: 'PMS/Users.txt' file not found.")
        return None

def add_log_entry(username):
    with open("PMS/Logs.txt", "a", encoding="utf8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {username} logged in.\n")

def add_logout_entry(username):
    logout_time = datetime.now()
    last_login_time = None

    try:
        with open("PMS/Logs.txt", "r", encoding="utf8") as file:
            # Find the last login entry for this specific user
            for line in reversed(file.readlines()):
                if username in line and "logged in" in line: # Bug fix: "Logged in" -> "logged in"
                    timestamp_str = line.split(" - ")[0]
                    last_login_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    break
    except FileNotFoundError:
        pass # If no log file, just proceed to create one
    except Exception as e:
        print(f"An error occurred while reading the log file: {e}")

    with open("PMS/Logs.txt", "a", encoding="utf8") as file:
        time_str = logout_time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{time_str} - {username} logged out.\n")

        if last_login_time:
            duration = logout_time - last_login_time
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            duration_parts = []
            if hours > 0:
                duration_parts.append(f"{hours} hour(s)")
            if minutes > 0:
                duration_parts.append(f"{minutes} minute(s)")
            if seconds > 0 or not duration_parts:
                 duration_parts.append(f"{seconds} second(s)")

            duration_str = ", ".join(duration_parts)
            file.write(f"    Session Duration: {duration_str}\n")

def quit_session(username):
    if username:
        print(f"Logging out {username}...")
        add_logout_entry(username)
    else:
        print("Quitting...")

def add_user():
    username = input("Enter a new username: ")
    password = input("Enter a new password for the user: ")
    with open("PMS/Users.txt", "a", encoding="utf8") as file:
        file.write(f"{username}-{password}\n")
    print(f"User '{username}' was added successfully.")

def add_admin():
    admin_name = input("Enter new admin username: ")
    admin_password = input("Enter new admin password: ")
    with open("PMS/Admins.txt", "a", encoding="utf8") as file:
        file.write(f"{admin_name}-{admin_password}\n")
    print(f"Admin '{admin_name}' added successfully.")

def list_users():
    print("\n--- User List ---")
    try:
        with open("PMS/Users.txt", "r", encoding="utf8") as file:
            users = file.readlines()
            if not users:
                print("No users found.")
            for user in users:
                print(user.strip().split('-')[0]) # Only show username
    except FileNotFoundError:
        print("No registered users found.")

def list_admins():
    print("\n--- Admin List ---")
    try:
        with open("PMS/Admins.txt", "r", encoding="utf8") as file:
            admins = file.readlines()
            if not admins:
                print("No admins found.")
            for admin in admins:
                print(admin.strip().split('-')[0]) # Only show admin name
    except FileNotFoundError:
        print("No registered admins found.")
