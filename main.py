import tkinter as tk
import tkinter.filedialog as filedialog
from audio_recorder import AudioRecorder
from audio_transcriber import AudioTranscriber


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        self.audio_recorder = None

    def create_widgets(self):
        self.rec_button = tk.Button(self, text="Record", command=self.start_recording)
        self.rec_button.grid(row=0, column=0)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1)

        self.time_label = tk.Label(self, text="Recording time (seconds):")
        self.time_label.grid(row=1, column=0)

        self.time_entry = tk.Entry(self)
        self.time_entry.grid(row=1, column=1)

        self.save_button = tk.Button(self, text="Save", command=self.save_file, state=tk.DISABLED)
        self.save_button.grid(row=2, column=0)

        self.transcribe_button = tk.Button(self, text="Transcribe", command=self.transcribe_audio, state=tk.DISABLED)
        self.transcribe_button.grid(row=2, column=1)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid(row=3, column=1)

    def start_recording(self):
        try:
            record_time = int(self.time_entry.get())
            if record_time <= 0:
                raise ValueError("Invalid recording time.")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
            return

        self.audio_recorder = AudioRecorder(record_time)
        self.rec_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.transcribe_button.config(state=tk.DISABLED)
        self.audio_recorder.record()

    def stop_recording(self):
        self.audio_recorder.stop()
        self.rec_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.transcribe_button.config(state=tk.NORMAL)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".wav")
        if file_path:
            self.audio_recorder.save(file_path)

    def transcribe_audio(self):
        file_path = filedialog.askopenfilename(defaultextension=".wav")
        if file_path:
            transcriber = AudioTranscriber(file_path)
            text = transcriber.transcribe()
            with open("transcription.txt", "w") as f:
                f.write(text)
            tk.messagebox.showinfo("Transcription", f"Transcribed text:\n{text}")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
