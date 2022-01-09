from typing import List


class Definition:
    def __init__(self):
        self._meaning = ''
        self._chinese = ''
        self._examples = []

    def set_meaning(self, meaning: str):
        self._meaning = meaning

    def set_chinese(self, chinese: str):
        self._chinese = chinese

    def set_examples(self, examples: List[str]):
        self._examples = examples

    def meaning(self) -> str:
        return self._meaning

    def chinese(self) -> str:
        return self._chinese

    def examples(self) -> List[str]:
        return self._examples

    def __str__(self):
        return f"{self._meaning}\n{self._chinese}\n{self._examples}"


class Word:
    def __init__(self):
        self._title = ""
        self._ipas = []
        self._sound_file_name = ""
        self._definitions = []

    def set_title(self, title: str):
        self._title = title

    def set_ipas(self, ipas: List[str]):
        self._ipas = ipas

    def set_sound_file_name(self, sound_file_name: str):
        self._sound_file_name = sound_file_name

    def set_definitions(self, definitions: List[Definition]):
        self._definitions = definitions

    def title(self) -> str:
        return self._title

    def ipas(self) -> List[str]:
        return self._ipas

    def sound_file_name(self) -> str:
        return self._sound_file_name

    def definitions(self) -> List[Definition]:
        return self._definitions

    def __str__(self):
        res = f"{self._title}\n{self._ipas}"
        for definition in self._definitions:
            res += "\n"
            res += str(definition)
        return res
