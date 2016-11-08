from app import app, config
from flask import render_template, request, redirect, url_for
import os, json
from app import setup
import psycopg2

pg_conn = config.get('LocalStorage')



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        setup.run()
        next_endpoint = 'projects'
        return next_endpoint

    conn = psycopg2.connect(**pg_conn)
    cur = conn.cursor()
    cur.execute('''select status from actions where action = 'setup';''')
    setup_made = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('index.html', setup=setup_made)


@app.route('/plain')
def plain():
    dns = config.get('Instance')['PublicDNS']
    port = config.get('Instance')['ShinyPort']
    protocol = config.get('Instance')['Protocol']

    address = '{0}://{1}:{2}/001-hello/'.format(protocol, dns, port)

    ds = request.args.get('dataset')
    return render_template('plain_page.html', dataset=ds,
                                        analysis_address=address)


@app.route('/analyses')
def analyses():
    return render_template('analyses.html')
