
from flask import Flask, render_template, request, jsonify
from automation import (
    open_application,
    open_website,
    close_application,
    take_screenshot,
    open_folder,
    search_files,
    shutdown_laptop,
    restart_laptop
)
from ai_engine import ask_ai
import webbrowser
from urllib.parse import quote_plus

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/status")
def status():
    return jsonify({
        "assistant": "Abhinav AI",
        "status": "Online",
        "language": "English"
    })


@app.route("/command", methods=["POST"])
def command():

    data = request.get_json() or {}
    user_command = data.get("command", "").strip().lower()

    if not user_command:
        return jsonify({"response": "Please enter a command."})

    # Close Applications
    if user_command.startswith("close "):
        app_name = user_command.replace("close ", "", 1).strip()
        response = close_application(app_name)

    # Screenshot
    elif any(phrase in user_command for phrase in [
        "screenshot", "screen shot", "take screenshot",
        "take a screenshot", "take screen shot",
        "take a screen shot"
    ]):
        response = take_screenshot()

    # Shutdown and Restart - safe mode
    elif user_command in ["shutdown", "shut down", "shutdown laptop"]:
        response = shutdown_laptop()

    elif user_command in ["restart", "restart laptop"]:
        response = restart_laptop()

    # Google Search
    elif user_command.startswith("search "):
        query = user_command.replace("search ", "", 1).strip()

        if query:
            webbrowser.open(
                "https://www.google.com/search?q=" + quote_plus(query)
            )
            response = f"Searching Google for {query}."
        else:
            response = "Please tell me what to search."

    # YouTube Search
    elif user_command.startswith("play "):
        query = user_command.replace("play ", "", 1).strip()

        if query:
            webbrowser.open(
                "https://www.youtube.com/results?search_query="
                + quote_plus(query)
            )
            response = f"Searching YouTube for {query}."
        else:
            response = "Please tell me what to play."

    # File Search
    elif user_command.startswith("find ") or user_command.startswith("search file"):
        response = search_files(user_command)

    # Open Folders
    elif any(folder in user_command for folder in [
        "downloads", "desktop", "documents",
        "pictures", "music", "videos"
    ]):
        response = open_folder(user_command)

    # Open Websites or Applications
    elif user_command.startswith("open "):
        target = user_command.replace("open ", "", 1).strip()

        if target in ["chrome", "notepad", "calculator"]:
            response = open_application(target)
        else:
            response = open_website(target)

    # Laptop Automation
    elif "notepad" in user_command:
        response = open_application("notepad")

    elif "calculator" in user_command:
        response = open_application("calculator")

    elif "chrome" in user_command:
        response = open_application("chrome")

    else:
        response = ask_ai(user_command)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
