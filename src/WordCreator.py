import Utils
from Word import Definition
from Word import Word

from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
import requests
import re


class IWordCreator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, word: str) -> Word: raise NotImplementedError


class CambridgeCrawlerWordCreator(IWordCreator):
    dictionary_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
    user_agent = "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"

    def create(self, word: str) -> Word:
        with requests.get(self.dictionary_url + word, headers={'user-agent': self.user_agent},
                          allow_redirects=True) as request:
            soup = BeautifulSoup(request.content, features="html.parser")

            result = Word()
            # get the title
            result.set_title(soup.find("meta", property="og:title")["content"])
            Utils.log('title: ' + result.title())

            if not self.__is_word_found(soup):
                raise Exception

            # get the IPA
            ipas = []
            for pron in soup.find_all('span', {'class': 'pron'}):
                Utils.log('pron: ' + pron.text)
                ipas.append(pron.text)
            result.set_ipas(ipas)
            Utils.log(result.ipas())

            # get the sound
            audio_url = self.__get_audio_url(soup)
            if audio_url:
                result.set_sound_file_name(f"{result.title()}-{Utils.get_time_str()}.mp3")
                self.__download_audio_file(audio_url, result.sound_file_name())

            # get the meaning
            definitions = []
            for meaning in soup.find_all('div', {'class': 'ddef_h'}):
                definitions.append(self.__create_definition(meaning))
            result.set_definitions(definitions)

            return result

    @staticmethod
    def __is_word_found(soup: BeautifulSoup) -> bool:
        url = soup.find("meta", property="og:url")["content"]
        not_found = bool(re.search("spellcheck$", str(url)))
        return not not_found

    @staticmethod
    def __get_audio_url(soup: BeautifulSoup) -> str:
        for src in soup.find_all('source'):
            if bool(re.search('\.mp3', str(src))):
                result = src.attrs['src']
                Utils.log("Found audio source: " + result)
                return result
        return ""

    @classmethod
    def __download_audio_file(cls, url: str, name: str):
        audio_url = "https://dictionary.cambridge.org/zht" + url
        with requests.get(audio_url, headers={'user-agent': cls.user_agent}) as request:
            with open(Utils.get_output_base() + name, "wb") as file:
                file.write(request.content)

    @staticmethod
    def __create_definition(meaning) -> Definition:
        result = Definition()

        result.set_meaning(meaning.text)
        Utils.log('meaning: ' + result.meaning())
        # chinese
        result.set_chinese(meaning.next_sibling.find('span', {'lang': 'zh-Hant'}).text)
        Utils.log('chinese: ' + result.chinese())
        # examples
        examples = []
        for example in meaning.next_sibling.find_all('div', {'class': 'examp'}):
            examples.append(re.sub('\n$', '', example.text))
        Utils.log(examples)
        result.set_examples(examples)

        return result
