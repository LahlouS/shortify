import os
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import time
import sys
from word import Word


class VoskDriver:

    def __init__(self, audio_filename, voskPath):
        if not os.path.exists(audio_filename):
            print(f"ERROR: File '{audio_filename}' doesn't exist . . .")
            sys.exit()
        self.filename = audio_filename
        if not os.path.exists(voskPath):
            print(f'ERROR: path to vosk model is not valid !')
            sys.exit()
        self.model_path = voskPath

        self.wf = wave.open(audio_filename, "rb")
        print(f"'{audio_filename} was successfully read'")
        # check if audio is mono wav
        if self.wf.getnchannels() != 1 or self.wf.getsampwidth() != 2 or self.wf.getcomptype() != "NONE":
            print("ERROR: Audio file must be WAV format mono PCM.")
            sys.exit()
        self.model = Model(self.model_path)
        self.rec = KaldiRecognizer(self.model, self.wf.getframerate())
        self.rec.SetWords(True)
    
    def process_audio(self):
        start_time = time.time()
        self.results = []
        self.text = ''
        while True:
            data = self.wf.readframes(4000)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                part_result = json.loads(self.rec.Result())
                self.results.append(part_result)

        part_result = json.loads(self.rec.FinalResult())
        self.results.append(part_result)

        for r in self.results:
            self.text += r['text'] + ' '
        time_elapsed = time.strftime(
        '%H:%M:%S', time.gmtime(time.time() - start_time))
        print(f'Done! Elapsed time = {time_elapsed}')
        
    def write_text(self, filename):
        with open(filename, "w") as text_file:
            text_file.write(self.text)
        print(f"Text successfully saved")

    def write_time_stamp(self, filename):
        list_of_words = []
        for sentence in self.results:
            if len(sentence) == 1:
                # sometimes there are bugs in recognition 
                # and it returns an empty dictionary
                # {'text': ''}
                continue
            for obj in sentence['result']:
                w = Word(obj)  # create custom Word object
                list_of_words.append(w)  # and add it to list
        with open(filename, "a") as TimeStampFile:
            TimeStampFile.write(f'\n\n########## {filename} ###############\n\n')
            for word in list_of_words:
                TimeStampFile.write(word.to_string() + '\n')
            TimeStampFile.write('\n\n########## EOF ###############\n\n')


