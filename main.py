import threading
import time
import tkinter as tk
import pyaudio
import wave
import os


class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()

        self.label_time = tk.Label(text="00:00:00")
        self.label_time.pack()
        self.label_time.place(x=250, y=180, anchor="center")
        self.root.resizable(False, False)
        self.root.title("Voice Recorder")
        self.root.geometry('500x400')

        self.button1 = tk.Button(text="Start", font=("Times news roman", 30, "bold"), command=self.start)
        self.button1.pack(side="bottom", padx=30, pady=30)
        self.recording = False
        self.root.mainloop()

    def start(self):
        if self.recording:
            self.recording = False
            self.button1.config(fg="black")
            self.label_time.config(fg="black")
            print(self.recording)
        else:
            self.recording = True
            self.button1.config(fg="red")
            self.label_time.config(fg="red")
            threading.Thread(target=self.record).start()


    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,rate= 44100, channels=1,input=True, frames_per_buffer=1024)

        frame = []

        start = time.time()

        while self.recording:
            data = stream.read(1024)
            frame.append(data)

            passed = time.time() - start

            secs = passed % 60
            mins = passed // 60
            hours = mins // 60

            self.label_time.config(text=f"{int(hours):02d} {int(mins):02d} {int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exist = True
        i = 1

        while exist:
            if os.path.exists(f"recording{i}.wav"):
                i += 1
            else:
                exist = False
        sound_file = wave.open(f"recording{i}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frame))
        sound_file.close()





VoiceRecorder()
