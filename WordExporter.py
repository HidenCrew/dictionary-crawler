from abc import ABCMeta, abstractmethod
import codecs
from enum import Enum
from typing import List

from Log import log
from Word import Word


class IWordExporter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def export(self, words: List[Word]): raise NotImplementedError

    class Format(Enum):
        docx = 1
        anki = 2


class DocxExporter(IWordExporter):
    def export(self, words):
        print("not implemented")


class Anki4000EEWExporter(IWordExporter):
    def export(self, words):
        with codecs.open("anki_words.txt", "w", "utf-8") as f:
            for word in words:
                f.write(word.title + ",")
                # this is an empty image
                f.write("\"\"" + ",")
                # todo: download sound
                # this is an empty sound
                f.write("\"\"" + ",")
                # this is an empty sound meaning
                f.write("\"\"" + ",")
                # this is an empty example sound
                f.write("\"\"" + ",")
                # meaning
                f.write("\"")
                examples = []
                for definition in word.definitions:
                    f.write("{}\n".format(definition.meaning))
                    f.write(u"{}\n".format(definition.chinese))
                    for example in definition.examples:
                        examples.append(example)
                f.write("\"" + ",")
                # example
                f.write("\"")
                for example in examples:
                    f.write(u"{}\n".format(example))
                f.write("\"" + ",")
                # pronounce
                f.write("\"")
                for pron in word.pronunciations:
                    f.write("{} ".format(pron))
                f.write("\"")
                # word end
                f.write("\n")


def getExporter(exportFormat: IWordExporter.Format) -> IWordExporter:
    if exportFormat == IWordExporter.Format.docx:
        return DocxExporter()
    elif exportFormat == IWordExporter.Format.anki:
        return Anki4000EEWExporter()
    else:
        raise Exception("Format error, input format: {}".format(exportFormat))


def export(words: List[Word], exportFormat: IWordExporter.Format):
    exporter = getExporter(exportFormat)
    exporter.export(words)