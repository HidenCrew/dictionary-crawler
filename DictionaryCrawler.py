from Word import Word
from WordExporter import export, IWordExporter
from Utils import log
from Utils import read_clean_words

raw_words = read_clean_words()
log(raw_words)

# Processing
words = []
for raw_word in raw_words:
    try:
        word = Word(raw_word)
        log(word)
        words.append(word)
    except:
        print(f"\"{raw_word}\" not found")


# todo: add unit test
export(words, IWordExporter.Format.anki)
