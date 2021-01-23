import requests
import copy
import sys
from bs4 import BeautifulSoup
import time

start = time.perf_counter()
s = requests.session()

class Translation:
    word_dic = {"1": "Arabic", "2": "German", "3": "English", "4": "Spanish", "5": "French",
                "6": "Hebrew", "7": "Japanese", "8": "Dutch", "9": "Polish", "10": "Portuguese", "11": "Romanian",
                "12": "Russian", "13": "Turkish"}
    from_, to_, word, url= "", "", "", ""
    r, soup = "",""

    def choices(self):
        print('''Hello, you're welcome to the translator. Translator supports: 
    1. Arabic
    2. German
    3. English
    4. Spanish
    5. French
    6. Hebrew
    7. Japanese
    8. Dutch
    9. Polish
    10. Portuguese
    11. Romanian
    12. Russian
    13. Turkish
    ''')
        return

    def input(self):
        print('Type the number of your language: ')
        self.from_ = input()
        print("Type the number of a language you want to translate to or '0' to translate to all languages:")
        self.to_ = input()
        print("Type the word you want to translate:")
        self.word = input()
        print()

    def url_(self, lang=""):
        if lang:
            b = lang
        else:
            b = self.to_

        self.url = f"https://context.reverso.net/translation/{self.from_}-{b}/{self.word}"
        user_agent = 'Mozilla/5.0'
        try:
            self.r = s.get(self.url.lower(), headers={'User-Agent': user_agent})
            if self.r.status_code != 200:
                print(f"Sorry, unable to find {self.word} ")
                exit()
        except requests.exceptions.ConnectionError:
            print("Something wrong with your internet")
            exit()
        return self.url


        # else:
        #     print(self.r.status_code)


    def translated_word(self):
        c = self.soup.find('div', {'id': 'translations-content'})
        word_list = [word for word in c.text.split()]
        return word_list


    def examples(self):
        sections = self.soup.find('section', {'id': 'examples-content'})
        example_list = [span.text.strip() for span in sections.find_all('span', {'class': 'text'})]
        return example_list



    def file_write(self, lang):
        connecter = open(f"{self.word}.txt", "a", encoding="utf-8")
        word = self.translated_word()
        sentence_ = self.examples()
        text_lines= [lang+" Translations:", word[0],"", lang +" examples:", sentence_[0]+ ":", sentence_[1], "\n"]
        for line in text_lines:
            connecter.write(line +"\n")
        connecter.close()




    def simultaneous_translation(self):
        temp_dict = copy.deepcopy(self.word_dic)
        pop_ = list(self.word_dic.keys())[list(self.word_dic.values()).index(self.from_)]
        temp_dict.pop(pop_)
        for lang in temp_dict.values():
            self.url = self.url_(lang)
            user_agent = 'Mozilla/5.0'
            self.r = s.get(self.url.lower(), headers={'User-Agent': user_agent})
            self.soup = BeautifulSoup(self.r.content, 'html.parser')
            self.file_write(lang)

        c = open(f"{self.word}.txt", "r",  encoding="utf-8")
        for line in c:
            print(line.strip())
        c.close()





    def main(self):
        # self.choices()
        # self.input()
        self.from_ = from_.capitalize()
        self.to_ = to_
        self.word = word_

        if self.to_.capitalize() not in self.word_dic.values() and self.to_ !="all":
            print(f"Sorry, the program doesn't support {self.to_}")
            exit()

        if self.to_ != "all":
            self.url_()
            self.soup = BeautifulSoup(self.r.content, 'html.parser')
            # translated = self.word_dic[self.to_]
            word_translated = self.translated_word()
            sentences = self.examples()
            # print('\nContext examples:\n')
            print(f'{self.to_} Translations:')
            print(*[word_translated[i]for i in range(5)], sep="\n")

            print(f'\n{self.to_} Examples:')
            for i in range(10):
                print(sentences[i])
                if i % 2 == 1:
                    print()
        else:
            self.simultaneous_translation()



translator = Translation()
if __name__ =="__main__":
    args = sys.argv
    from_ = args [1]
    to_ = args[2]
    word_ = args[3]

    translator.main()
    end = time.perf_counter()
