from Word import Word
from WordExporter import export, IWordExporter
from Utils import log

# put in words
rawWords = ['Compound interest']
log(rawWords)

# Processing
words = []
for rawWord in rawWords:
    try:
        word = Word(rawWord)
        log(word)
        words.append(word)
    except:
        print("\"{}\" not found".format(rawWord))


# todo: add unit test
export(words, IWordExporter.Format.anki)
