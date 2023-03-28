import pyaudio
import wave


class AudioRecorder:
    def __init__(self, record_time):
        self.record_time = record_time
        self.frames = []
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk_size = 1024
        self.audio_interface = pyaudio.PyAudio()
        self.stream = None

    def record(self):
        self.stream = self.audio_interface.open(format=self.sample_format,
                                                 channels=self.channels,
                                                 rate=self.sample_rate,
                                                 frames_per_buffer=self.chunk_size,
                                                 input=True)
        for i in range(int(self.sample_rate / self.chunk_size * self.record_time)):
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio_interface.terminate()

    def save(self, file_path):
        with wave.open(file_path, "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.audio_interface.get_sample_size(self.sample_format))
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(b"".join(self.frames))
