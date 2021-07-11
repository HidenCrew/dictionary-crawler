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
        return "{}\n{}\n{}".format(self.meaning, self.chinese, self.examples)


class Word:
    dictionaryUrl = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
    userAgent = "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"

    def __init__(self, word):
        with requests.get(Word.dictionaryUrl + word, headers={'user-agent': Word.userAgent}, allow_redirects=True) as request:
            soup = BeautifulSoup(request.content)

            # get the title
            self.title = soup.find("meta", property="og:title")["content"]
            Utils.log('title: ' + self.title)

            if not self.isWordFound(soup):
                raise Exception

            # get the IPA
            self.ipas = []
            for pron in soup.find_all('span', {'class': 'pron'}):
                Utils.log('pron: ' + pron.text)
                self.ipas.append(pron.text)
            Utils.log(self.ipas)

            # get the sound
            self.soundFileName = ""
            audioUrl = self.getAudioUrl(soup)
            if audioUrl:
                self.soundFileName = "{}-{}.mp3".format(self.title, Utils.getTimeStr())
                self.downloadAudioFile(audioUrl)

            # get the meaning
            self.definitions = []
            for meaning in soup.find_all('div', {'class': 'ddef_h'}):
                self.definitions.append(Definition(meaning))

    def isWordFound(self, soup: BeautifulSoup) -> bool:
        url = soup.find("meta", property="og:url")["content"]
        return bool(re.search("{}$".format(self.title), str(url)))

    def getAudioUrl(self, soup: BeautifulSoup) -> str:
        for src in soup.find_all('source'):
            if bool(re.search('\.mp3', str(src))):
                result = src.attrs['src']
                Utils.log("Found audio source: " + result)
                return result
        return ""

    def downloadAudioFile(self, url: str):
        audioUrl = "https://dictionary.cambridge.org/zht" + url
        with requests.get(audioUrl, headers={'user-agent': Word.userAgent}) as request:
            with open(Utils.getOutputBase() + self.soundFileName, "wb") as file:
                file.write(request.content)

    def __str__(self):
        res = "{}\n{}".format(self.title, self.ipas)
        for definition in self.definitions:
            res += "\n"
            res += str(definition)
        return res