import requests
from bs4 import BeautifulSoup
def corrector(word):
    r = requests.get('https://www.google.ro/search?q=' + word)
    soup = BeautifulSoup(r.text, 'html.parser')
    main = soup.find(id = 'main')
    #print(main)
    cnt = main.find_all('i')
    links = main.find_all('a')
    i = 0
    if len(cnt) != 0:
        for href in links:
            if(str(href.get('href')).find(str(cnt[0].get_text().replace(' ','+')))) != -1:
                print(str(href.get('href')))
                break
            i = i + 1

        word_corrected = str(links[i].get('href')).split('q=')[1].split('&')[0].replace('+',' ') # parse google autocorrect 

    with open('output.txt', 'w') as file:
        file.write(word + '\n')
        if len(cnt) != 0:
            file.write("Sugestie: " + word_corrected)

    #print(r.text)
corrector('am luat')