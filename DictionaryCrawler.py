from Word import Word
from WordExporter import export, IWordExporter

# put in words
rawWords = ['test']
# print(rawWords)

# Processing
words = []
for rawWord in rawWords:
    word = Word(rawWord)
    print(word)
    words.append(word)

export(words, IWordExporter.Format.anki)