# convenient package
import re
import ytScript
import cutVideo

# speechRecognition

from voskDriver import VoskDriver
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

if len(sys.argv) != 3:
    print('ERROR: wrong args:\n>> python [basename] [url]')
    sys.exit()
SetLogLevel(0)

url = sys.argv[2]

outpath = 'video/'
path = 'input/'
base_filename = sys.argv[1]

video_filename = path + base_filename
audio_filename = path + base_filename

video_ext = '.mp4'
audio_ext = '.wav'

text_filename = "audioTranslate/video_to_text.txt"
timestamp_filename = "audioTranslate/video_txt_time_stamp.txt"

ytScript.dl_video_audio(url, base_filename)

model_path = "voskModel/vosk-model-en-us-0.22"

######### TEXT RECOGNITION ############ 

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

