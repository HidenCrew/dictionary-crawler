import requests
from bs4 import BeautifulSoup
import re


class Definition:
    def __init__(self, meaning):
        self.meaning = meaning.text
        print('meaning: ' + self.meaning)
        # chinese
        self.chinese = meaning.next_sibling.find('span', {'lang': 'zh-Hant'}).text
        print('chinese: ' + self.chinese)
        # examples
        self.examples = []
        for example in meaning.next_sibling.find_all('div', {'class': 'examp'}):
            self.examples.append(re.sub('\n$', '', example.text))
        print(self.examples)

    def __str__(self):
        return "{}\n{}\n{}".format(self.meaning, self.chinese, self.examples)


class Word:
    def __init__(self, word):
        # Make the request to a url
        dictionary_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
        user_agent = "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"
        r = requests.get(dictionary_url + word, headers={'user-agent': user_agent})
        soup = BeautifulSoup(r.content)

        # get the title
        title = soup.find('title').text
        print('raw title: ' + title)
        self.title = re.sub(' \|.*', '', title)
        print('clean title: ' + self.title)

        # get the pronunciation
        self.pronunciations = []
        for pron in soup.find_all('span', {'class': 'pron'}):
            print('pron: ' + pron.text)
            self.pronunciations.append(pron.text)
        print(self.pronunciations)

        # get the meaning
        self.definitions = []
        for meaning in soup.find_all('div', {'class': 'ddef_h'}):
            self.definitions.append(Definition(meaning))

    def __str__(self):
        return "{}\n{}\n{}".format(self.title, self.pronunciations, self.definitions)


# put in words
rawWords = ['test']
print(rawWords)

# Processing
for rawWord in rawWords:
    word = Word(rawWord)
    print(word)
