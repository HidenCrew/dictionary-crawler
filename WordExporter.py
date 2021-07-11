from abc import ABCMeta, abstractmethod
import codecs
from enum import Enum
from typing import List

from Utils import log
from Utils import getTimeStr
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


# todo: open file to output directory, and the audio file too
class Anki4000EEWExporter(IWordExporter):
    separator = ","

    def export(self, words):
        with codecs.open("anki-{}.txt".format(getTimeStr()), "w", "utf-8") as f:
            for word in words:
                f.write(word.title + Anki4000EEWExporter.separator)
                # this is an empty image
                f.write("\"\"" + Anki4000EEWExporter.separator)
                # this is an empty sound
                if word.soundFileName:
                    f.write("\"[sound:{}]\"".format(word.soundFileName) + Anki4000EEWExporter.separator)
                else:
                    f.write("\"\"" + Anki4000EEWExporter.separator)
                # this is an empty sound meaning
                f.write("\"\"" + Anki4000EEWExporter.separator)
                # this is an empty example sound
                f.write("\"\"" + Anki4000EEWExporter.separator)
                # meaning
                f.write("\"")
                examples = []
                for definition in word.definitions:
                    f.write("{}\n".format(definition.meaning))
                    f.write(u"{}\n".format(definition.chinese))
                    for example in definition.examples:
                        examples.append(example)
                f.write("\"" + Anki4000EEWExporter.separator)
                # example
                f.write("\"")
                for example in examples:
                    f.write(u"{}\n".format(example))
                f.write("\"" + Anki4000EEWExporter.separator)
                # pronounce
                f.write("\"")
                for pron in word.ipas:
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