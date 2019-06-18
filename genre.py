import requests
from bs4 import BeautifulSoup

genres = {}
with open('genres.txt') as f:
    if f.readable():
        key = f.readline()
        while key:
            name = f.readline()
            key = int(key)
            name = name.replace('\n','')
            genres[key] = name
            key = f.readline()

def get_genre_name(genre_num):
    # finding the genres name from their number by requesting to the best-podcasts url
    # do this iff there's no records in the genres.txt
    if genre_num not in genres:
        result = requests.get(f"https://www.listennotes.com/best-podcasts/{genre_num}/")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        h1 = soup.h1.text
        h1 = h1.replace('Best ','')
        h1 = h1.replace('Podcasts','')
        h1 = h1.replace('\n','')
        h1 = h1.replace('\n','')
        genres[genre_num] = h1
        print(genres[genre_num])
        with open('genres.txt', 'a') as f:
            f.write(str(genre_num))
            f.write('\n')
            f.write(genres[genre_num])
            f.write('\n')

    return genres[genre_num]