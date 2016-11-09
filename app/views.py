from app import app, config
from flask import render_template, request, redirect, url_for
import os, json
from app import setup
import psycopg2

pg_conn = config.get('LocalStorage')



def check_actions():
    conn = psycopg2.connect(**pg_conn)
    cur = conn.cursor()
    cur.execute('''select status from actions where action = 'setup';''')
    setup_made = cur.fetchone()
    cur.close()
    conn.close()

    return setup_made


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', setup=True)


@app.route('/analyses/<string:dataset>')
def plain(dataset=None):
    dns = config.get('Instance')['PublicDNS']
    port = config.get('Instance')['ShinyPort']
    protocol = config.get('Instance')['Protocol']

    address = '{0}://{1}:{2}/{3}/'.format(protocol, dns, port, dataset)

    return render_template('plain_page.html', dataset=dataset,
                                        analysis_address=address)


@app.route('/analyses')
def analyses():
    return render_template('analyses.html')
