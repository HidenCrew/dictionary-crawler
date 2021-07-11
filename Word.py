from Utils import log
from Utils import getTimeStr

import requests
from bs4 import BeautifulSoup
import re


# todo: word and definition should be a data structure, and we should not put the parsing code in there constructor
#  => createWordFrom...?
class Definition:
    def __init__(self, meaning):
        self.meaning = meaning.text
        log('meaning: ' + self.meaning)
        # chinese
        self.chinese = meaning.next_sibling.find('span', {'lang': 'zh-Hant'}).text
        log('chinese: ' + self.chinese)
        # examples
        self.examples = []
        for example in meaning.next_sibling.find_all('div', {'class': 'examp'}):
            self.examples.append(re.sub('\n$', '', example.text))
        log(self.examples)

    def __str__(self):
        return "{}\n{}\n{}".format(self.meaning, self.chinese, self.examples)


class Word:
    dictionaryUrl = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
    userAgent = "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"

    def __init__(self, word):
        # Make the request to a url
        r = requests.get(Word.dictionaryUrl + word, headers={'user-agent': Word.userAgent})
        soup = BeautifulSoup(r.content)

        # get the title
        title = soup.find('title').text
        log('raw title: ' + title)
        self.title = re.sub(' \|.*', '', title)
        log('clean title: ' + self.title)

        # get the IPA
        self.ipas = []
        for pron in soup.find_all('span', {'class': 'pron'}):
            log('pron: ' + pron.text)
            self.ipas.append(pron.text)
        log(self.ipas)

        # get the sound
        self.soundFileName = ""
        audioUrl = self.getAudioUrl(soup)
        if audioUrl:
            self.soundFileName = "{}-{}.mp3".format(self.title, getTimeStr())
            self.downloadAudioFile(audioUrl)

        # get the meaning
        self.definitions = []
        for meaning in soup.find_all('div', {'class': 'ddef_h'}):
            self.definitions.append(Definition(meaning))

    def getAudioUrl(self, soup: BeautifulSoup) -> str:
        for src in soup.find_all('source'):
            if bool(re.search('\".*mp3\"', str(src))):
                result = src.attrs['src']
                log("Found audio source: " + result)
                return result
        return ""

    def downloadAudioFile(self, url: str):
        audioUrl = "https://dictionary.cambridge.org/zht" + url
        with requests.get(audioUrl, headers={'user-agent': Word.userAgent}) as request:
            with open(self.soundFileName, "wb") as file:
                file.write(request.content)

    def __str__(self):
        res = "{}\n{}".format(self.title, self.ipas)
        for definition in self.definitions:
            res += "\n"
            res += str(definition)
        return res