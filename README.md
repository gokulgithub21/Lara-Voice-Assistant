# 🎙️ Lara - Your Personal Voice Assistant

Lara is a cross-platform intelligent voice assistant built using Python. It listens to your commands, performs tasks like playing music, opening applications, telling jokes, reading news, setting alarms, and more—all through natural voice commands.

![Lara UI Preview](https://i.imgur.com/J9LK7Qi.png)

---

## 🚀 Features

- Voice-activated assistant with GUI using Tkinter
- Speech recognition using `speech_recognition`
- Text-to-speech using `pyttsx3`
- Smart commands:
  - Open local and web apps
  - Email sending
  - System control (volume, brightness, minimize/maximize)
  - News reading via RSS
  - Screenshot capturing
  - File/folder creation
  - Telling jokes, IP check, and more
- Alarm system
- Wake word: **"Lara"**

---

## 🧰 Requirements

### Python Packages:
- `speechrecognition`
- `pyttsx3`
- `pyaudio`
- `plyer`
- `feedparser`
- `psutil`
- `wmi` (Windows only)
- `requests`
- `pillow`
- `pyautogui`
- `playsound`

Install all required packages:

```bash
pip install -r requirements.txt
