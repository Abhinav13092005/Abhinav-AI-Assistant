
import os
import webbrowser
from urllib.parse import quote_plus

from flask import Flask, render_template, request, jsonify
from ai_engine import ask_ai

# Windows automation imports
if os.name == "nt":
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
else:
    open_application = None
    open_website = None
    close_application = None
    take_screenshot = None
    open_folder = None
    search_files = None
    shutdown_laptop = None
    restart_laptop = None


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/status")
def status():
    return jsonify({
        "assistant": "Abhinav AI",
        "status": "Online",
        "language": "English",
        "mode": "Live AI Chat" if os.name != "nt" else "Local Windows Assistant"
    })


@app.route("/command", methods=["POST"])
def command():

    data = request.get_json(silent=True) or {}
    user_command = str(data.get("command", "")).strip().lower()

    if not user_command:
        return jsonify({
            "response": "Please enter a command."
        })

    # Live server: allow AI chat, not laptop automation
    if os.name != "nt":

        if user_command.startswith(("open ", "close ", "find ", "search file")):
            response = (
                "Laptop automation is available only when "
                "Abhinav AI is running locally on your Windows laptop."
            )

        elif user_command in [
            "shutdown", "shut down", "shutdown laptop",
            "restart", "restart laptop"
        ]:
            response = "Shutdown and restart are disabled for safety."

        elif any(word in user_command for word in [
            "screenshot", "screen shot"
        ]):
            response = "Screenshot capture is available in local mode only."

        else:
            response = ask_ai(user_command)

        return jsonify({"response": response})

    # Local Windows automation

    if user_command.startswith("close "):
        app_name = user_command.replace("close ", "", 1).strip()
        response = close_application(app_name)

    elif any(phrase in user_command for phrase in [
        "screenshot", "screen shot", "take screenshot",
        "take a screenshot", "take screen shot",
        "take a screen shot"
    ]):
        response = take_screenshot()

    elif user_command in ["shutdown", "shut down", "shutdown laptop"]:
        response = shutdown_laptop()

    elif user_command in ["restart", "restart laptop"]:
        response = restart_laptop()

    elif user_command.startswith("search "):
        query = user_command.replace("search ", "", 1).strip()

        if query:
            webbrowser.open(
                "https://www.google.com/search?q=" + quote_plus(query)
            )
            response = f"Searching Google for {query}."
        else:
            response = "Please tell me what to search."

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

    elif user_command.startswith(("find ", "search file")):
        response = search_files(user_command)

    elif any(folder in user_command for folder in [
        "downloads", "desktop", "documents",
        "pictures", "music", "videos"
    ]):
        response = open_folder(user_command)

    elif user_command.startswith("open "):
        target = user_command.replace("open ", "", 1).strip()

        if target in ["chrome", "notepad", "calculator"]:
            response = open_application(target)
        else:
            response = open_website(target)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
