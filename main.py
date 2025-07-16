import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import random
import smtplib
import ssl
from email.message import EmailMessage
from plyer import notification
import time
import subprocess
import socket
import pyautogui
import feedparser
import psutil
import wmi
import threading
import requests
from io import BytesIO
from tkinter import *
from PIL import Image, ImageTk
from playsound import playsound
from plyer import notification

# ====================== CONFIGURATION ======================
# Paths
music_folder = "music"
memory_file = "memory.txt"

# Web applications mapping
WEB_APPS = {
    "word": "https://www.office.com/launch/word",
    "excel": "https://www.office.com/launch/excel",
    "powerpoint": "https://www.office.com/launch/powerpoint",
    "vs code": "https://vscode.dev",
    "visual studio code": "https://vscode.dev",
    "spotify": "https://open.spotify.com",
    "paint": "https://jspaint.app",
    "settings": "ms-settings:"
}

# Jokes
jokes = [
    "Why don't scientists trust atoms? Because they make up everything.",
    "I told my computer I needed a break, and it said 'no problem — I'll go to sleep.'",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Why don’t programmers like nature? It has too many bugs.",
    "How does a computer get drunk? It takes screenshots.",
    "Why do Java developers wear glasses? Because they don’t C#.",
    "What do you call 8 hobbits? A hobbyte.",
    "Why was the math book sad? It had too many problems.",
    "I asked the IT guy, 'How do you make a motherboard?' He said, 'I tell her about my job.'",
    "Parallel lines have so much in common… it’s a shame they’ll never meet.",
    "Why did the computer show up at work late? It had a hard drive.",
    "How do robots pay for things? With cache.",
    "What’s a computer’s least favorite food? Spam.",
    "Why was the cell phone wearing glasses? Because it lost its contacts.",
    "What did one wall say to the other wall? 'I'll meet you at the corner.'",
    "What’s orange and sounds like a parrot? A carrot.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "What did the zero say to the eight? Nice belt!",
    "What do you get when you cross a snowman and a vampire? Frostbite.",
    "Why did the bicycle fall over? Because it was two-tired!"
]


# ====================== UI CLASS ======================
class AssistantUI:  
    def __init__(self, root):
        self.root = root
        self.root.title("Lara Assistant")
        self.root.geometry("400x600")
        self.root.configure(bg='#0a192f')
        
        # Load logo
        try:
            response = requests.get("https://i.imgur.com/J9LK7Qi.png")
            img = Image.open(BytesIO(response.content))
            img = img.resize((150, 150), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(img)
        except:
            self.logo = PhotoImage(width=150, height=150)
        
        # UI Elements
        self.logo_label = Label(root, image=self.logo, bg='#0a192f')
        self.logo_label.pack(pady=20)
        
        self.status_label = Label(root, text="Say 'Lara' to wake me up", 
                               font=('Helvetica', 12), fg='white', bg='#0a192f')
        self.status_label.pack(pady=10)
        
        self.animation_label = Label(root, text="", font=('Helvetica', 24), 
                                   fg='#64ffda', bg='#0a192f')
        self.animation_label.pack(pady=20)
        
        self.command_label = Label(root, text="", font=('Helvetica', 10), 
                                 fg='#ccd6f6', bg='#0a192f', wraplength=380)
        self.command_label.pack(pady=10, padx=10)
        
        # Animation variables
        self.animating = False
        self.animation_sequence = ["•", "••", "•••", "••••"]
        self.animation_index = 0
        
    def update_status(self, text):
        self.status_label.config(text=text)
        
    def update_command(self, text):
        self.command_label.config(text=text)
        
    def start_animation(self):
        if not self.animating:
            self.animating = True
            self.animate()
            
    def stop_animation(self):
        self.animating = False
        self.animation_label.config(text="")
        
    def animate(self):
        if self.animating:
            self.animation_label.config(text=self.animation_sequence[self.animation_index])
            self.animation_index = (self.animation_index + 1) % len(self.animation_sequence)
            self.root.after(300, self.animate)

# ====================== ASSISTANT FUNCTIONS ======================
def speak(text):
    print(f"Assistant: {text}")
    ui.update_command(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Text-to-speech error:", e)

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        ui.update_status("🎤 Listening...")
        ui.start_animation()
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio).lower().strip()
            print(f"You said: {command}")
            ui.update_command(f"You said: {command}")
            ui.stop_animation()
            return command
        except sr.WaitTimeoutError:
            print("⏰ Listening timed out.")
            ui.stop_animation()
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            ui.stop_animation()
            return ""
        except sr.RequestError:
            speak("Speech service is not available.")
            ui.stop_animation()
            return ""

def send_email(to_email, subject, body):
    try:
        EMAIL = "gokuls0607@gmail.com"
        PASSWORD = "ghcn jlgb ceah bzvu"
        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        speak("Email has been sent successfully.")
    except Exception as e:
        print("Email error:", e)
        speak("Sorry, I could not send the email.")

def play_music():
    try:
        songs = os.listdir(music_folder)
        if songs:
            song_path = os.path.join(music_folder, random.choice(songs))
            speak("Playing music")
            os.startfile(song_path)
        else:
            speak("No music found in your music folder.")
    except Exception as e:
        speak("Could not play music.")
        print(e)

def normalize_time_input(input_str):
    # Remove spaces and convert to lowercase
    input_str = input_str.replace(" ", "").lower()
    
    # Add colon if user says time like "237" → "2:37"
    if input_str.isdigit() and len(input_str) in [3, 4]:
        if len(input_str) == 3:
            input_str = f"0{input_str[0]}:{input_str[1:]}"
        else:
            input_str = f"{input_str[:2]}:{input_str[2:]}"
    
    # Add AM or PM if not specified (optional improvement)
    return input_str

def set_alarm(alarm_time):
    try:
        dt = datetime.datetime.strptime(alarm_time, "%H:%M")
        alarm_time_24hr = dt.strftime("%H:%M")
    except ValueError:
        speak("I couldn't understand the time format. Please try again in HH:MM format.")
        return

    speak(f"Alarm set for {alarm_time_24hr}")
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == alarm_time_24hr:
            speak("Wake up! This is your alarm.")
            notification.notify(
                title="⏰ Alarm",
                message="Wake up! It's time!",
                timeout=10
            )
            try:
                playsound("alarm.mp3")
            except Exception as e:
                print("Error playing sound:", e)
            break
        time.sleep(10)

        
def open_any_app(app_name):
    app_name = app_name.lower().strip()

    # Special case for Command Prompt
    if app_name in ["cmd", "command prompt"]:
        try:
            subprocess.Popen('start cmd', shell=True)
            speak("Opening Command Prompt")
            return
        except Exception as e:
            speak("Failed to open Command Prompt")
            print(f"Error opening cmd: {e}")
            return

    # Known app paths
    known_apps = {
        "notepad": "notepad.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "ms edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "microsoft edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "spotify": "spotify.exe",
        "vs code": r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getlogin()),
        "visual studio code": r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getlogin()),
        "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
        "ppt": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "settings": "ms-settings:",
        "file explorer": "explorer.exe",
        "this pc": "explorer.exe",
    }

    try:
        if app_name in known_apps:
            app_path = known_apps[app_name]
            if os.path.exists(app_path) or app_path.startswith("ms-settings:") or not app_path.endswith(".exe"):
                try:
                    if app_path.startswith("ms-settings:"):
                        subprocess.Popen(f'start {app_path}', shell=True)
                    else:
                        subprocess.Popen(app_path if app_path.endswith(".exe") or os.path.isabs(app_path) else [app_path], shell=True)
                    speak(f"Opening {app_name}")
                    return
                except Exception as e:
                    print(f"Error opening {app_name}: {e}")


        # If not found, fallback to web version if available
        if app_name in WEB_APPS:
            speak(f"{app_name} not found locally. Opening in browser.")
            webbrowser.open(WEB_APPS[app_name])
        else:
            speak(f"Sorry, I couldn't find an application named {app_name}.")
    except Exception as e:
        speak(f"Failed to open {app_name}")
        print(f"Error: {e}")


def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    speak(f"Your IP address is {ip_address}")

def take_screenshot():
    screenshots_dir = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    file_name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    file_path = os.path.join(screenshots_dir, file_name)
    pyautogui.screenshot(file_path)
    speak(f"Screenshot taken and saved as {file_name} on Pictures\Screenshots")

def read_rss_news():
    speak("Fetching latest news headlines.")
    urls = [
        "https://feeds.feedburner.com/ndtvnews-top-stories",
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "https://www.thehindu.com/news/national/feeder/default.rss"
    ]
    headlines = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            headlines.extend([entry.title for entry in feed.entries[:2]])
        except:
            continue
    if headlines:
        speak("Here are some top headlines:")
        for i, headline in enumerate(headlines[:5], 1):
            speak(f"Headline {i}: {headline}")
    else:
        speak("Sorry, couldn't fetch news right now.")

def handle_command(command):
    if not command:
        return "continue"
        
    command = command.lower()
    
    if 'time' in command or 'what is time now' in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    
    elif 'date' in command or 'what date today' in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")
    
    elif 'search youtube' in command or 'youtube search' in command:
        speak("What do you want to search on YouTube?")
        query = listen_command()
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
    
    elif 'search google' in command or 'google search' in command:
        query = command.replace("search google", "").replace("google search", "").replace("for", "").strip()
        if not query:
            speak("What do you want to search on Google?")
            query = listen_command()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")

    elif 'set alarm' in command:
        speak("What time should I set the alarm for? Please say in 24-hour format like 18:30")
        alarm_time = listen_command()
        if alarm_time:
            threading.Thread(target=set_alarm, args=(alarm_time,), daemon=True).start()

    
    elif 'open spotify' in command and 'play' in command:
        song = command.replace("open spotify and play", "").strip()
        if song:
            webbrowser.open(f"https://open.spotify.com/search/{song.replace(' ', '%20')}")
            speak(f"Playing {song} on Spotify")
    
    elif 'open' in command:
        app_name = command.replace("open", "").strip()
        if app_name:
            open_any_app(app_name)
        else:
            speak("Please specify an application to open")
    
    elif 'minimize window' in command or 'minimize this window' in command or 'minimise window' in command or 'minimise this window' in command:
        pyautogui.hotkey('win', 'down')
        speak("Window minimized")
    
    elif 'maximize window' in command or 'maximize this window' in command or 'maximise window' in command or 'maximise this window' in command:
        pyautogui.hotkey('win', 'up')
        speak("Window maximized")
    
    elif 'close window' in command or 'close this window' in command:
        pyautogui.hotkey('alt', 'f4')
        speak("Window closed")
    
    elif 'increase volume' in command or 'volume up' in command:
        for _ in range(5):
            pyautogui.press("volumeup")
        speak("Volume increased")
    
    elif 'decrease volume' in command or 'volume down' in command:
        for _ in range(5):
            pyautogui.press("volumedown")
        speak("Volume decreased")
    
    elif 'mute' in command or 'unmute' in command:
        pyautogui.press("volumemute")
        speak("Volume toggled")

    elif 'increase brightness' in command or 'brightness up' in command:
        try:
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            current = c.WmiMonitorBrightness()[0].CurrentBrightness
            new_brightness = min(100, current + 10)
            methods.WmiSetBrightness(new_brightness, 0)
            speak(f"Brightness increased to {new_brightness}%")
        except Exception as e:
            print("Brightness control error:", e)
            speak("Sorry, I couldn't adjust the brightness")

    elif 'decrease brightness' in command or 'brightness down' in command:
        try:
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            current = c.WmiMonitorBrightness()[0].CurrentBrightness
            new_brightness = max(0, current - 10)
            methods.WmiSetBrightness(new_brightness, 0)
            speak(f"Brightness decreased to {new_brightness}%")
        except Exception as e:
            print("Brightness control error:", e)
            speak("Sorry, I couldn't adjust the brightness")
    
    
    elif 'create folder' in command:
        speak("What should be the folder name?")
        name = listen_command()
        if name:
            try:
                os.makedirs(name, exist_ok=True)
                speak(f"Folder '{name}' created successfully in the current directory.")
            except Exception as e:
                speak("Failed to create folder")
                print(e)
    
    elif 'create file' in command:
        speak("What should be the file name?")
        name = listen_command()
        if name:
            try:
                with open(name + ".txt", 'w') as f:
                    pass
                speak(f"File '{name}.txt' created successfully in the current directory.")
            except Exception as e:
                speak("Failed to create file")
                print(e)
    
    elif 'ip address' in command or 'my ip' in command:
        get_ip()
    
    elif 'take screenshot' in command or 'capture screen' in command:
        take_screenshot()
    
    elif 'news' in command or 'headlines' in command:
        read_rss_news()
    
    elif 'tell me a joke' in command or 'joke' in command:
        joke = random.choice(jokes)
        speak(joke)
    
    elif any(word in command for word in ['exit', 'quit', 'bye', 'goodbye']):
        speak("Goodbye! Have a nice day.")
        return "exit"
    
    elif any(word in command for word in ['sleep', 'stop listening','Bye Lara','i will catch you later']):
        speak("Going back to sleep mode. Say 'Lara' when you need me.")
        return "sleep"
    
    else:
        speak("Sorry, I didn't understand that command.Can you please repeat?")

    return "continue"

def run_assistant():
    def get_time_based_greeting():
        current_hour = datetime.datetime.now().hour
        if 5 <= current_hour < 12:
            return "Have a wonderful morning!"
        elif 12 <= current_hour < 17:
            return "Have a great afternoon!"
        elif 17 <= current_hour < 21:
            return "Have a pleasant evening!"
        else:
            return "Have a good night and sweet dreams!"

    def assistant_thread():
        speak("Hello! I am Lara, Say 'Lara' to wake me up.")
        while True:
            try:
                wake_command = listen_command()
                if wake_command and "Lara" in wake_command or "lara" in wake_command:
                    speak("Yes, I'm listening. Say 'sleep' to stop or 'exit' to quit.")
                    while True:
                        command = listen_command()
                        if not command:
                            continue
                        result = handle_command(command)
                        if result == "exit":
                            greeting = get_time_based_greeting()
                            speak(f"Goodbye! {greeting}")
                            root.quit()
                            return
                        if result == "sleep":
                            speak("Going to sleep mode. Say 'Lara' when you need me.")
                            break
                else:
                    print("Wake word not detected.")
            except KeyboardInterrupt:
                greeting = get_time_based_greeting()
                speak(f"Goodbye! {greeting}")
                root.quit()
                return
            except Exception as e:
                print(f"Error in main loop: {e}")
                speak("Sorry, I encountered an error. Restarting...")

    threading.Thread(target=assistant_thread, daemon=True).start()
    root.mainloop()
# ====================== MAIN EXECUTION ======================
if __name__ == "__main__":
    root = Tk()
    ui = AssistantUI(root)
    run_assistant()