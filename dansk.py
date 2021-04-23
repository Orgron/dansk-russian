import webbrowser
import requests, bs4
import re

ru='ЦцАаБбВвГгДдЕеЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЪъЬьЩщ ЖжЫыЭэЁёЧчШшЮюЯя'
la = ['c', 'c', 'a', 'a', 'b', 'b', 'v', 'v', 'g', 'g', 'd', 'd', 'e', 'e', 'z', 'z', 'i', 'i', 'j', 'j', 'k', 'k', 'l', 'l',
      'm', 'm', 'n', 'n', 'o', 'o', 'p', 'p', 'r', 'r', 's', 's', 't', 't', 'u', 'u', 'f', 'f', 'x', 'x', '#', '#', "'", "'",
      'w', 'w', '-', 'zh', 'zh', 'yi', 'yi', 'ye', 'ye', 'yo', 'yo', 'ch', 'ch', 'sh', 'sh', 'yu', 'yu', 'ya', 'ya']

def remove_n(s, leave=1):
    s1 = len(s)
    s2 = len(s)
    while(True):
        # print('before',len(definition))
        s = s.replace('\n'*(leave+1),'\n'*leave)
        # print(len(definition))
        s1 = s2
        s2 = len(s)
        if s1 == s2: break
    return s

def ddo_tags(tag):
    if tag.name == 'div':
        classes = tag.get("class", [])
        ids = tag.get("id")
        return "definitionBox" in classes and str(ids).startswith('betydning')

def slovar_tags(tag):
    if tag.name == "td":
        valign = str(tag.get("valign"))
        width = str(tag.get("width"))
        # print(valign, width)
        return "middle" in valign # and not "200" in width

while(True):

    language = input('Choose the language (D for Danish, R for Russian): ')
    word = input('Type your word: ')

    if language == 'D':
        res_ddo = requests.get('https://ordnet.dk/ddo/ordbog?query='+word, headers={'User-Agent': 'Mozilla/5.0'})
        noStarchSoup_ddo = bs4.BeautifulSoup(res_ddo.text, 'html.parser')
        elems_ddo = noStarchSoup_ddo.find_all(ddo_tags)
        definitions = [e.text for e in elems_ddo]
        # print(elems_ddo[0])

        for i in range(len(definitions)):
            definitions[i] = remove_n(definitions[i])
            print(f'{i+1}.',definitions[i])
            c = input()
            if c == "stop": break

        res_slovar = requests.get('http://www.slovar.dk/tdansk/'+word, headers={'User-Agent': 'Mozilla/5.0'})
        res_slovar.encoding = 'cp1251'
        noStarchSoup_slovar = bs4.BeautifulSoup(res_slovar.text, 'html.parser')
        elems_slovar = noStarchSoup_slovar.find_all(slovar_tags)
        # print(elems_slovar)
        translations = [e.text for e in elems_slovar]

        for i in range(1,len(translations),2):
            translations[i-1] = remove_n(translations[i-1], leave=0)
            translations[i] = remove_n(translations[i], leave=0)
            print(f'{i//2+1}.',translations[i-1], translations[i])
            c = input()
            if c == "stop": break
        #webbrowser.open('https://ordnet.dk/ddo/ordbog?query='+word)
        #webbrowser.open('http://www.slovar.dk/tdansk/'+word)
    elif language == 'R':

        n_word=''
        
        for i in range(len(word)):
            s = word[i]
            if s in ru:
                s = la[ru.find(s)]
            n_word += s
        print(n_word)
        res_slovar = requests.get('http://www.slovar.dk/trussisk/'+n_word, headers={'User-Agent': 'Mozilla/5.0'})
        res_slovar.encoding = 'cp1251'
        noStarchSoup_slovar = bs4.BeautifulSoup(res_slovar.text, 'html.parser')
        elems_slovar = noStarchSoup_slovar.find_all(slovar_tags)
        # print(elems_slovar)
        translations = [e.text for e in elems_slovar]

        for i in range(1,len(translations),2):
            translations[i-1] = remove_n(translations[i-1], leave=0)
            translations[i] = remove_n(translations[i], leave=0)
            print(f'{i//2+1}.',translations[i-1], translations[i])
            c = input()
            if c == "stop": break
        #webbrowser.open('http://www.slovar.dk/trussisk/'+word)
        

