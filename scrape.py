import requests, csv
from pprint import pprint
import time
from app import config
import psycopg2

pg_conn = config.get('LocalStorage')
conn = psycopg2.connect(**pg_conn)
cur = conn.cursor()


with open('datasets/movies.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    sf_movies = [row for row in reader]


URL = 'http://www.omdbapi.com/'

movies = {}
for movie in sf_movies:
    if movie['Title'] not in movies:
        movies[movie['Title']] = {'Title': movie['Title'], 'Year': movie['Release Year']}

print('Movies to scrape:', len(movies))


imdb = []
for i,(title, movie) in enumerate(movies.items()):
    print(movie['Title'], movie['Year'])

    payload = dict(t=movie['Title'], y=movie['Year'], plot='Full', r='json')

    resp = requests.get(URL, params=payload)
    imdb.append(resp.json())

    print(sorted(resp.json().keys()))

    pprint(resp.json())
    print('\n\n\n')

    time.sleep(0.3)
    break



with open('datasets/imdb.csv', 'w') as csvfile:
    fieldnames = imdb[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(imdb)


query = 'create table imdb as '
query = "copy {} from '{}' with csv header null 'NULL'".format(
                                table, filename_fullpath)

cur.execute(query)

# make sure data will persist
conn.commit()



cur.close()
conn.close()
