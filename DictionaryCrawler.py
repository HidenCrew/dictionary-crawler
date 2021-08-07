from Word import Word
from WordExporter import export, IWordExporter
from Utils import log

# put in words
raw_words = ['australia']
log(raw_words)

# Processing
words = []
for raw_word in raw_words:
    try:
        word = Word(raw_word)
        log(word)
        words.append(word)
    except:
        print("\"{}\" not found".format(raw_word))


# todo: add unit test
export(words, IWordExporter.Format.anki)
