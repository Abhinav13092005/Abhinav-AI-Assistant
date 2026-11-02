
const listenBtn = document.getElementById("listenBtn");
const sendBtn = document.getElementById("sendBtn");
const commandInput = document.getElementById("commandInput");
const responseText = document.getElementById("responseText");
const statusText = document.getElementById("status");
const historyList = document.getElementById("historyList");

let isListening = false;
let isProcessing = false;
let lastCommandTime = 0;
let recognition = null;
let commandHandled = false;

function addHistory(command) {
    const item = document.createElement("li");
    item.textContent = command;
    historyList.prepend(item);
}

function speakResponse(text) {
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 0.9;
    speech.volume = 1;

    speech.onstart = () => {
        statusText.textContent = "Abhinav AI is speaking...";
    };

    speech.onend = () => {
        statusText.textContent = "Abhinav AI is ready";
    };

    window.speechSynthesis.speak(speech);
}

async function sendCommand(command) {
    command = command.trim();

    const now = Date.now();

    if (!command || isProcessing) return;
    if (now - lastCommandTime < 2000) return;

    lastCommandTime = now;
    isProcessing = true;

    listenBtn.disabled = true;
    sendBtn.disabled = true;

    statusText.textContent = "Abhinav AI is processing...";
    responseText.textContent = "Please wait...";

    addHistory(command);

    try {
        const response = await fetch("/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ command: command })
        });

        const data = await response.json();

        responseText.textContent = data.response;
        speakResponse(data.response);

    } catch (error) {
        responseText.textContent =
            "Unable to connect to Abhinav AI server.";
        statusText.textContent = "Connection error";

    } finally {
        isProcessing = false;
        listenBtn.disabled = false;
        sendBtn.disabled = false;
    }
}

// Text command
sendBtn.addEventListener("click", () => {
    const command = commandInput.value.trim();

    if (command) {
        commandInput.value = "";
        sendCommand(command);
    }
});

// Enter key
commandInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendBtn.click();
    }
});

// Voice command
listenBtn.addEventListener("click", () => {

    if (isListening || isProcessing) return;

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        responseText.textContent =
            "Speech recognition is not supported. Please use Chrome.";
        return;
    }

    recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    commandHandled = false;
    isListening = true;

    let finalTranscript = "";

    listenBtn.disabled = true;
    statusText.textContent = "Abhinav AI is listening...";
    responseText.textContent = "Speak your complete command in English.";

    recognition.onresult = (event) => {

        let interimTranscript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {

            const transcript = event.results[i][0].transcript;

            if (event.results[i].isFinal) {
                finalTranscript += transcript + " ";
            } else {
                interimTranscript += transcript;
            }
        }

        const currentText =
            (finalTranscript + interimTranscript).trim();

        commandInput.value = currentText;
        responseText.textContent = currentText || "Listening...";
    };

    recognition.onerror = (event) => {
        isListening = false;
        listenBtn.disabled = false;

        statusText.textContent = "Voice recognition error";
        responseText.textContent =
            "Please try again. Error: " + event.error;
    };

    recognition.onend = () => {

        isListening = false;
        listenBtn.disabled = false;

        if (commandHandled) return;

        commandHandled = true;

        const command = finalTranscript.trim();

        if (!command) {
            statusText.textContent = "Abhinav AI is ready";
            responseText.textContent =
                "No complete command detected. Please try again.";
            return;
        }

        commandInput.value = command;

        if (command.toLowerCase() === "open") {
            statusText.textContent = "Incomplete command";
            responseText.textContent =
                "Please say a complete command, for example Open Notepad.";
            return;
        }

        sendCommand(command);
    };

    try {
        recognition.start();
    } catch (error) {
        isListening = false;
        listenBtn.disabled = false;
        statusText.textContent = "Unable to start microphone.";
    }
});
