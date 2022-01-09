import WordCreator
from WordExporter import export, IWordExporter
from WordNotFoundException import WordNotFoundException
from Utils import log
from Utils import read_clean_words

raw_words = read_clean_words()
log(raw_words)

# Processing
factory = WordCreator.CambridgeCrawlerWordCreator()
words = []
for raw_word in raw_words:
    try:
        word = factory.create(raw_word)
        log(word)
        words.append(word)
    except WordNotFoundException as e:
        print(e)


# todo: add unit test
#  1. sample with example sentence, meaning...
#  2. sample that can't be found correctly
export(words, IWordExporter.Format.anki)
