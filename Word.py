import Utils

import requests
from bs4 import BeautifulSoup
import re


# todo: word and definition should be a data structure, and we should not put the parsing code in there constructor
#  => createWordFrom...? or WordFactory, CambridgeCrawlerWordFactory
class Definition:
    def __init__(self, meaning):
        self.meaning = meaning.text
        Utils.log('meaning: ' + self.meaning)
        # chinese
        self.chinese = meaning.next_sibling.find('span', {'lang': 'zh-Hant'}).text
        Utils.log('chinese: ' + self.chinese)
        # examples
        self.examples = []
        for example in meaning.next_sibling.find_all('div', {'class': 'examp'}):
            self.examples.append(re.sub('\n$', '', example.text))
        Utils.log(self.examples)

    def __str__(self):
        return f"{self.meaning}\n{self.chinese}\n{self.examples}"


class Word:
    dictionary_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
    user_agent = "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"

    def __init__(self, word):
        with requests.get(Word.dictionary_url + word, headers={'user-agent': Word.user_agent}, allow_redirects=True) as request:
            soup = BeautifulSoup(request.content)

            # get the title
            self.title = soup.find("meta", property="og:title")["content"]
            Utils.log('title: ' + self.title)

            if not self.is_word_found(soup):
                raise Exception

            # get the IPA
            self.ipas = []
            for pron in soup.find_all('span', {'class': 'pron'}):
                Utils.log('pron: ' + pron.text)
                self.ipas.append(pron.text)
            Utils.log(self.ipas)

            # get the sound
            self.sound_file_name = ""
            audio_url = self.get_audio_url(soup)
            if audio_url:
                self.sound_file_name = f"{self.title}-{Utils.get_time_str()}.mp3"
                self.download_audio_file(audio_url)

            # get the meaning
            self.definitions = []
            for meaning in soup.find_all('div', {'class': 'ddef_h'}):
                self.definitions.append(Definition(meaning))

    def is_word_found(self, soup: BeautifulSoup) -> bool:
        url = soup.find("meta", property="og:url")["content"]
        not_found = bool(re.search("spellcheck$", str(url)))
        return not not_found

    def get_audio_url(self, soup: BeautifulSoup) -> str:
        for src in soup.find_all('source'):
            if bool(re.search('\.mp3', str(src))):
                result = src.attrs['src']
                Utils.log("Found audio source: " + result)
                return result
        return ""

    def download_audio_file(self, url: str):
        audio_url = "https://dictionary.cambridge.org/zht" + url
        with requests.get(audio_url, headers={'user-agent': Word.user_agent}) as request:
            with open(Utils.get_output_base() + self.sound_file_name, "wb") as file:
                file.write(request.content)

    def __str__(self):
        res = f"{self.title}\n{self.ipas}"
        for definition in self.definitions:
            res += "\n"
            res += str(definition)
        return res