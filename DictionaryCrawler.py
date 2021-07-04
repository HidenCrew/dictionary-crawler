from Word import Word
from WordExporter import export, IWordExporter
from Log import log

# put in words
rawWords = ['run-up', 'arbitrate', 'dispute', 'synchronized swimming',
            'athletics', 'catastrophic', 'disrupt', 'unprecedented',
            'spectator', 'litigation', 'precedent']
log(rawWords)

# Processing
words = []
for rawWord in rawWords:
    word = Word(rawWord)
    print(word)
    words.append(word)


# todo: add unit test
# todo: fail case handle: 404 not found...? to English version to check again first
export(words, IWordExporter.Format.anki)

