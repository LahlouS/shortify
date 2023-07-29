# convenient package
import re
import ytScript
import cutVideo

# speechRecognition
import os
import sys
import time
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from word import Word

# textRank

import spacy
import pytextrank
import sys
from punctuator import Punctuator

# cutting video

import ffmpeg


SetLogLevel(0)

url = 'https://www.youtube.com/watch?v=ofeg1P0yHUQ&pp=ygUPd29sZnJhbSBwaHlzaWNz'

outpath = 'video/'
path = 'input/'
base_filename = 'trump'

video_filename = path + base_filename
audio_filename = path + base_filename

video_ext = '.mp4'
audio_ext = '.wav'

text_filename = "audioTranslate/video_to_text.txt"
timestamp_filename = "audioTranslate/video_txt_time_stamp.txt"

ytScript.dl_video_audio(url, base_filename)

model_path = "voskModel/vosk-model-en-us-0.22"

# if not os.path.exists(audio_filename):
#     print(f"ERROR: File '{audio_filename}' doesn't exist . . .")
#     sys.exit()

# print(f"Reading your file '{audio_filename}'...")

# # reading audio file using wave module
# wf = wave.open(audio_filename, "rb")
# print(f"'{audio_filename} was successfully read'")

# # check if audio is mono wav
# if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#     print("ERROR: Audio file must be WAV format mono PCM.")
#     sys.exit()

# # READING THE MODEL

# if not os.path.exists(model_path):
#     print(f'ERROR: path to vosk model is not valid !')
#     sys.exit()

# print(f'reading vosk model \'{model_path}\'...')
# model = Model(model_path)
# rec = KaldiRecognizer(model, wf.getframerate())
# rec.SetWords(True)

# print('Start converting to text. It may take some time...')
# start_time = time.time()

# results = []

# while True:
#     data = wf.readframes(4000)
#     if len(data) == 0:
#         break
#     if rec.AcceptWaveform(data):
#         part_result = json.loads(rec.Result())
#         results.append(part_result)

# part_result = json.loads(rec.FinalResult())
# results.append(part_result)

# # RESULT IS OF TYPE:
# # [
# # {'result': [
#                 # {'conf': 1.0, 'end': 1.92, 'start': 1.5, 'word': 'some'},
#                 # {'conf': 1.0, 'end': 2.37, 'start': 1.92, 'word': 'speech'},
#                 # {'conf': 1.0, 'end': 3.09, 'start': 2.37, 'word': 'recognition'},
#                 #  . . .
# #             ],
# # 'text': "the text contained in the wf.readframes(4000) (see l.46)"
# # },
#     # . . . 
# # ]

# # 'conf' equals the rate of confident regarding the word
# # 'end' 'start' are the timeStamp
# # 'word' is the word we talk about

# # forming a final string from the words
# text = ''
# for r in results:
#     text += r['text'] + ' '

# time_elapsed = time.strftime(
#     '%H:%M:%S', time.gmtime(time.time() - start_time))
# print(f'Done! Elapsed time = {time_elapsed}')

# print("\tOUTPUT STRING:\n")
# print(text)

# print(f"Saving text to '{text_filename}'...")
# with open(text_filename, "w") as text_file:
#     text_file.write(text)
# print(f"Text successfully saved")

# print(f"Saving timstamp text to timestamp.'{text_filename}'...")
# list_of_words = []
# for sentence in results:
#     if len(sentence) == 1:
#         # sometimes there are bugs in recognition 
#         # and it returns an empty dictionary
#         # {'text': ''}
#         continue
#     for obj in sentence['result']:
#         w = Word(obj)  # create custom Word object
#         list_of_words.append(w)  # and add it to list

# with open(timestamp_filename, "a") as TimeStampFile:
#     TimeStampFile.write(f'\n\n########## {timestamp_filename} ###############\n\n')
#     for word in list_of_words:
#         TimeStampFile.write(word.to_string() + '\n')
#     TimeStampFile.write('\n\n########## EOF ###############\n\n')
#         # print(word.to_string())


# # NOW PROCESSING THE STRING WITH TEXT RANK

from voskDriver import VoskDriver

vd = VoskDriver(audio_filename + audio_ext, model_path)

vd.process_audio()
vd.write_text(text_filename)
vd.write_time_stamp(timestamp_filename)

text = vd.text
results = vd.results



p = Punctuator('Demo-Europarl-EN.pcl')
text = p.punctuate(text)
print("PUNCTUATED TEXT:\n", text)

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
#nlp.add_pipe("textrank")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN", "VERB"] } })

doc = nlp(text)
# examine the top-ranked phrases in the document
#for phrase in doc._.phrases:
#    print(phrase.text)
#    print(phrase.rank, phrase.count)
#    print(phrase.chunks)


print('\n\n')
highlight = 0
u = nlp(text)
for sentence in u.sents:
    # print('***', sentence, '***')
    if doc._.phrases[0].text in str(sentence):
        highlight =  [elem.lower() for elem in re.split('\ |\.|\, ', str(sentence)) if len(elem) > 0]
        print(f'{sentence}|')


print(f'{highlight}|')
print("############## HIGHLIGHT #########################")
print(highlight)


sentence_start_time_stamp = {}
sentence_end_time_stamp = {}
ret = 0
i = 0
for result in results:
    try:
        for stuff in result['result']:
            if stuff['word'] == highlight[i] and i != (len(highlight) - 1):
                if i == 0:
                    sentence_start_time_stamp = stuff
                i += 1
            elif stuff['word'] == highlight[i] and i == (len(highlight) - 1):
                sentence_end_time_stamp = stuff
                ret = 1
                break
            elif stuff['word'] != highlight[i]:
                i = 0
                pass
        if ret:
            break
            
            # print(stuff["word"])
    except KeyError as k:
        print('you have reach the end')
    
print('start: ', sentence_start_time_stamp)
print('end: ', sentence_end_time_stamp)

# NOW WE LOOK FOR CUTTING THE VIDEO WITH THE START AND END TIME
# filename = 'video/trump.mp4'
# ytScript.dlVideo(url, filename)

# fps = cutVideo.getFps(video_filename)
start_frame = float(sentence_start_time_stamp["start"])
end_frame = float(sentence_end_time_stamp["end"])

print('------> ', start_frame, end_frame)
command = 'ffmpeg -ss ' + str(start_frame * 1000) + 'ms' + ' -i ' + video_filename + video_ext + '  -c copy -c:a aac -b:a 128k -t ' + str((end_frame - start_frame) * 1000) + 'ms' + f' video/cut_{base_filename}.mp4'
os.system(command)

