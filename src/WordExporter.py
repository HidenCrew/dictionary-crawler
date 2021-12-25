import Utils
from Word import Word

from abc import ABCMeta, abstractmethod
import codecs
from enum import Enum
from typing import List


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
    separator = ","

    def export(self, words):
        with codecs.open(f"{Utils.get_output_base()}anki-{Utils.get_time_str()}.txt", "w", "utf-8") as f:
            for word in words:
                f.write(word.title + Anki4000EEWExporter.separator)
                # this is an empty image
                f.write("\"\"" + Anki4000EEWExporter.separator)
                # this is an empty sound
                if word.sound_file_name:
                    f.write(f"\"[sound:{word.sound_file_name}]\"" + Anki4000EEWExporter.separator)
                else:
                    f.write("\"\"" + Anki4000EEWExporter.separator)
                # this is an empty sound meaning
                f.write("\"\"" + Anki4000EEWExporter.separator)
                # this is an empty example sound
                f.write("\"\"" + Anki4000EEWExporter.separator)
                # todo: replace " with \", in case some example include "
                # meaning
                f.write("\"")
                examples = []
                for definition in word.definitions:
                    f.write(f"{definition.meaning}\n")
                    f.write(f"{definition.chinese}\n")
                    for example in definition.examples:
                        examples.append(example)
                f.write("\"" + Anki4000EEWExporter.separator)
                # example
                f.write("\"")
                for example in examples:
                    f.write(f'{example}\n')
                f.write("\"" + Anki4000EEWExporter.separator)
                # pronounce
                f.write("\"")
                for pron in word.ipas:
                    f.write(f"{pron} ")
                f.write("\"")
                # word end
                f.write("\n")


def get_exporter(export_format: IWordExporter.Format) -> IWordExporter:
    if export_format == IWordExporter.Format.docx:
        return DocxExporter()
    elif export_format == IWordExporter.Format.anki:
        return Anki4000EEWExporter()
    else:
        raise Exception(f"Format error, input format: {export_format}")


def export(words: List[Word], export_format: IWordExporter.Format):
    exporter = get_exporter(export_format)
    exporter.export(words)