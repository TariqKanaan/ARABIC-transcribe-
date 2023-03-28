import speech_recognition as sr


class AudioTranscriber:
    def __init__(self, file_path):
        self.file_path = file_path

    def transcribe(self):
        r = sr.Recognizer()

        with sr.AudioFile(self.file_path) as source:
            audio = r.record(source)

        text = r.recognize_google(audio)
        return text
