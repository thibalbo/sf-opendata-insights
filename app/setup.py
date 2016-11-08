import requests, re, os
from app import config
from pprint import pprint
import psycopg2

pg_conn = config.get('LocalStorage')
conn = psycopg2.connect(**pg_conn)
cur = conn.cursor()



class Flow:
    def __init__(self):
        self.tasks = []



class Datasets:
    """
    Download and copy specified datasets to Postgres.
    """
    def __init__(self):
        self.datasets = config.get('Datasets')
        self.dataset_filename = config.get('DatasetFilename')
        self.dataset_url = config.get('DatasetURL')
        self.pg_conn = config.get('LocalStorage')
        self.wdir = os.getcwd()


    def get_datasets(self):
        """
        Manage the datasets download flow.
        """
        for dataset in self.datasets:
            url = self.dataset_url.format(dataset['id'])
            self.download_dataset(url, dataset)
            self.create(dataset)


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


    def create(self, dataset):
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

        query = "copy {} from '{}' with csv header null 'NULL'".format(
                                        table, filename_fullpath)

        cur.execute(query)

        # make sure data will persist
        conn.commit()


    def run(self):
        print('Running setup...')
        self.get_datasets()
        print('Done.')









# response = requests.get(url)
# if response.status_code == 200:
#     data = response.json()
#
# for k, v in data[0].items():
#     print(k, type(v))


# import requests, csv
# from pprint import pprint
# import time
#
#
#
#
# with open('Film_Locations_in_San_Francisco.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     sf_movies = [row for row in reader]
#
#
# URL = 'http://www.omdbapi.com/'
#
# sf_movies = [{'Title': movie['Title'], 'Year': movie['Release Year']} for movie in sf_movies]
# print(sf_movies)
#
# # meta = []
# # for movie in sf_movies[:20]:
# #     print(movie['Title'], movie['Release Year'])
# #
# #     # payload = dict(t=movie['Title'], y=movie['Release Year'], plot='Full', r='json')
# #     #
# #     # resp = requests.get(URL, params=payload)
# #     # pprint(resp.json())
# #     # print('\n\n\n')
# #
# #     # time.sleep(3)



def run():
    print('Setup...')
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


if __name__ == '__main__':
    run()

# things to do: luigi for scheduling init queries
