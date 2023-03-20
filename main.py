from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import os
from tkinter import *
from tkinter import simpledialog, messagebox
import pyttsx3
import datetime
import socket


class TranscribeApp:
    def __init__(self, master):
        self.master = master
        master.title("Arabic Speech Transcription")
        master.geometry("600x400")
        master.config(bg="white")

        self.label = Label(master, text="Press the button to start speaking and transcribing.", font=("Helvetica", 16), bg="white")
        self.label.pack(pady=20)

        self.speak_button = Button(master, text="Start", command=self.listen, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.speak_button.pack(pady=10)

        self.save_button = Button(master, text="Save", command=self.save, font=("Helvetica", 14), bg="#2196F3", fg="white")
        self.save_button.pack(pady=10)

        self.pause_button = Button(master, text="adjust Microphone", command=self.pause_microphone, font=("Helvetica", 14), bg="#F44336", fg="white")
        self.pause_button.pack(pady=10)

        self.speak_text_button = Button(master, text="Speak Transcription", command=self.speak_transcription, font=("Helvetica", 14), bg="#9C27B0", fg="white")
        self.speak_text_button.pack(pady=10)

        self.output_text = Text(master, font=("Helvetica", 14), height=10)
        self.output_text.pack(pady=20, padx=50)

        self.r = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.engine = pyttsx3.init()

    def listen(self):
        with self.microphone as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, phrase_time_limit=10)

        try:
            transcription = self.r.recognize_google(audio, language="ar-SA")
            self.output_text.insert(END, transcription + '\n')

            obj = gTTS(text=transcription, lang='ar', slow=False)
            obj.save('text.mp3')
            playsound('text.mp3')

        except sr.UnknownValueError:
            messagebox.showinfo("Speech Recognition", "Unable to recognize speech")
        except sr.RequestError as e:
            messagebox.showerror("Speech Recognition", f"Could not request results from Google Speech Recognition service; {e}")

    def pause_microphone(self):
        self.r.energy_threshold = 4000  # a higher value means that the recognizer needs more noise to recognize words

    def speak_transcription(self):
        text = self.output_text.get("1.0", END)
        self.engine.say(text)
        self.engine.runAndWait()

    def save(self):
        filename = simpledialog.askstring("Save File", "Enter a filename:")
        if filename:
            filepath = os.path.join(os.getcwd(), f"{filename}.txt")
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(self.output_text.get("1.0", END))
                messagebox.showinfo("Save Successful", f"Transcription saved to {filepath}.")
        else:
            messagebox.showerror("Save Error", "Please enter a valid filename.")


if __name__ == '__main__':
    root = Tk()
    app = TranscribeApp(root)
    root.mainloop()
