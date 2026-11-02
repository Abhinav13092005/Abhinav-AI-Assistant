
import os
import webbrowser
import pyautogui
import subprocess
from datetime import datetime
from urllib.parse import urlparse


def open_application(command):

    command = command.lower().strip()

    if "chrome" in command:
        os.startfile("chrome.exe")
        return "Opening Google Chrome."

    elif "notepad" in command:
        os.startfile("notepad.exe")
        return "Opening Notepad."

    elif "calculator" in command:
        os.startfile("calc.exe")
        return "Opening Calculator."

    return "Application not available."


def open_website(command):

    command = command.lower().strip()

    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://github.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com"
    }

    for name, url in websites.items():

        if name in command:
            webbrowser.open(url)
            return f"Opening {name.capitalize()}."

    words = command.split()

    for word in words:

        if "." in word:

            website = word.strip(".,!?")

            if not website.startswith(("http://", "https://")):
                website = "https://" + website

            parsed = urlparse(website)

            if parsed.netloc and "." in parsed.netloc:
                webbrowser.open(website)
                return f"Opening {parsed.netloc}."

    return "Please provide a valid website name or address."


def close_application(command):

    command = command.lower().strip()

    apps = {
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "chrome": "chrome.exe"
    }

    for app_name, process_name in apps.items():

        if app_name in command:

            try:
                result = subprocess.run(
                    ["taskkill", "/IM", process_name, "/F"],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    return f"{app_name.capitalize()} closed successfully."

                return f"Could not close {app_name}. {result.stderr.strip()}"

            except Exception as e:
                return f"Error closing {app_name}: {e}"

    return "Please specify Notepad, Calculator, or Chrome."


def take_screenshot():

    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)

    filename = datetime.now().strftime(
        "screenshot_%Y%m%d_%H%M%S.png"
    )

    filepath = os.path.join(folder, filename)

    pyautogui.screenshot().save(filepath)

    return f"Screenshot saved: {filepath}"


# Open common Windows folders
def open_folder(command):

    command = command.lower().strip()

    folders = {
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
        "music": os.path.join(os.path.expanduser("~"), "Music"),
        "videos": os.path.join(os.path.expanduser("~"), "Videos")
    }

    for name, path in folders.items():

        if name in command:

            if os.path.isdir(path):
                os.startfile(path)
                return f"Opening {name.capitalize()} folder."

            return f"{name.capitalize()} folder was not found."

    return "Please specify Downloads, Documents, Desktop, Pictures, Music, or Videos."


# Search files inside common user folders
def search_files(command):

    command = command.lower().strip()

    extensions = {
        "pdf": ".pdf",
        "photo": (".jpg", ".jpeg", ".png", ".webp"),
        "image": (".jpg", ".jpeg", ".png", ".webp"),
        "picture": (".jpg", ".jpeg", ".png", ".webp"),
        "document": (".doc", ".docx", ".txt", ".pdf"),
        "word": (".doc", ".docx"),
        "excel": (".xls", ".xlsx", ".csv")
    }

    selected_extensions = None

    for name, ext in extensions.items():

        if name in command:
            selected_extensions = ext
            break

    if selected_extensions is None:
        return "Please specify a file type such as PDF, photo, document, or Excel."

    if isinstance(selected_extensions, str):
        selected_extensions = (selected_extensions,)

    search_locations = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Documents"),
        os.path.join(os.path.expanduser("~"), "Pictures")
    ]

    found_files = []

    for folder in search_locations:

        if not os.path.isdir(folder):
            continue

        for root, dirs, files in os.walk(folder):

            dirs[:] = [
                d for d in dirs
                if d.lower() not in ["node_modules", ".git", "__pycache__"]
            ]

            for filename in files:

                if filename.lower().endswith(selected_extensions):
                    found_files.append(os.path.join(root, filename))

                    if len(found_files) >= 20:
                        break

            if len(found_files) >= 20:
                break

        if len(found_files) >= 20:
            break

    if not found_files:
        return "No matching files found in Desktop, Downloads, Documents, or Pictures."

    result = "Files found:\n" + "\n".join(found_files)

    return result

def shutdown_laptop():
    return "Shutdown is disabled for safety. Please confirm before proceeding."


def restart_laptop():
    return "Restart is disabled for safety. Please confirm before proceeding."

