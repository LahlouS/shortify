import spacy
import pytextrank
import sys
from punctuator import Punctuator

# example text


text_filename = 'audioTranslate/outputSampleTextFile.txt'
with open(text_filename, "r") as text_file:
    rawtext = text_file.read()

print(f"NO PUNCTUATION:\n{rawtext}\n\n")

p = Punctuator('Demo-Europarl-EN.pcl')
text = p.punctuate(rawtext)
print("PUNCTUATED TEXT:\n", text)

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")

doc = nlp(text)
# examine the top-ranked phrases in the document
for phrase in doc._.phrases:
    print(phrase.text)
    print(phrase.rank, phrase.count)
    print(phrase.chunks)


print('\n\n')
u = nlp(text)
for sentence in u.sents:
    # print('***', sentence, '***')
    if doc._.phrases[0].text in str(sentence):
        print(sentence)