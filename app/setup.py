import requests, re, os
from app import config
from pprint import pprint
import psycopg2
import csv, time

pg_conn = config.get('LocalStorage')
conn = psycopg2.connect(**pg_conn)
cur = conn.cursor()



class Scrape:

    def save(self, dataset):
        with open('datasets/imdb.csv', 'w') as csvfile:
            fieldnames = sorted(dataset[0].keys())
            print(fieldnames)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)


    def scrape(self, meta):
        with open('datasets/movies.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            sf_movies = [row for row in reader]

        URL = 'http://www.omdbapi.com/'

        movies = {}
        for movie in sf_movies:
            if movie['Title'] not in movies:
                movies[movie['Title']] = {'Title': movie['Title'], 'Year': movie['Release Year']}

        print('Movies to scrape:', len(movies))


        cols = [c[0] for c in meta['columns']]
        imdb = []
        for i,(title, movie) in enumerate(movies.items()):
            print(i+1, movie['Title'])

            payload = dict(t=movie['Title'], y=movie['Year'], plot='Full', r='json')
            resp = requests.get(URL, params=payload)
            data = resp.json()

            resp_type = data.get('Response')
            if resp_type == 'Error':
                continue

            items = {}
            for k,v in data.items():
                if k in cols:
                    items[k] = v

            imdb.append(items)

            time.sleep(0.1)

        self.save(imdb)



class Datasets(Scrape):
    """
    Download and copy specified datasets to Postgres.
    """
    def __init__(self):
        self.datasets = config.get('Datasets')
        self.dataset_filename = config.get('DatasetFilename')
        self.dataset_url = config.get('DatasetURL')
        self.pg_conn = config.get('LocalStorage')
        self.wdir = os.getcwd()


    def download_dataset(self, url, dataset):
        """
        Download a dataset.

        :param url: link to download
        :param dataset: metadata from the specified dataset
        :returns: saved file path plus filename
        """
        filename = dataset['table']
        local_filename = self.dataset_filename.format(filename)

        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        return local_filename


    def create(self, dataset, null='NULL'):
        """
        Create table and copy data.

        :param dataset: metadata from the specified dataset
        """
        table = dataset['table']
        columns = dataset['columns']

        list_cols = ['{} {}'.format(col[0], col[1]) for col in columns]
        parsed_columns = ','.join(list_cols)

        # create table if not exists
        query = 'create table if not exists {} ({})'.format(
                                                table, parsed_columns)
        cur.execute(query)

        # copy data
        ds_filename = self.dataset_filename.format(table)
        filename_fullpath = '/'.join([self.wdir, ds_filename])

        query = "copy {} from '{}' with csv header null '{}'".format(
                                        table, filename_fullpath, null)

        cur.execute(query)
        conn.commit() # make sure data will persist


    def run(self):
        """
        Manage the datasets download flow.
        """
        print('Running setup...')
        for dataset in self.datasets:
            print(dataset['table'])

            if dataset['download']:
                url = self.dataset_url.format(dataset['id'])
                self.download_dataset(url, dataset)
                self.create(dataset)
            else:
                self.scrape(dataset)
                self.create(dataset, null='N/A')


        print('Done.')



def run():
    print('Setup...')

    os.system('mkdir datasets')
    os.system('mkdir db')

    query = '''create table if not exists actions (action text, status bool, ts timestamp without time zone default (now() at time zone 'utc'));'''
    cur.execute(query)

    cur.execute('''select status from actions where action = 'setup';''')
    exists = cur.fetchone()

    if not exists:
        print('Running setup...')
        ds = Datasets()
        ds.run()

        query = '''insert into actions (action, status) values ('setup', true)'''
        cur.execute(query)
    else:
        print('Setup already executed.')


    conn.commit()

    cur.close()
    conn.close()
