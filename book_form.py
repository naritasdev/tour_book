#!/usr/bin/env python
# coding: utf-8

## Copyright Humberto Yances, author. All rights reserved.

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import g
import flask_resize
import json
import sqlite3


app = Flask('book_form')
app.config['RESIZE_URL'] = 'http://localhost:9090/static'
app.config['RESIZE_ROOT'] = '/home/humberto/desarrollo/datos/hoteles/data_science/client_segm/apps/static'
resize = flask_resize.Resize(app)

DATABASE = 'tic.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        def make_dicts(cursor, row):
            return dict((cursor.description[idx][0], value)
                        for idx, value in enumerate(row))
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/book', methods=['GET'])
def book_tour():

    arg0 = request.args.get('em')
    arg1 = request.args.get('ht')
    arg2 = request.args.get('ag')
    arg3 = request.args.get('nm', 'Fulano')
    arg4 = request.args.get('ng', '1')
    arg5 = request.args.get('rc', '1')
    arg6 = request.args.get('ac', '3')

    cur = get_db().cursor()
    sql = 'SELECT * FROM tic WHERE id =' + arg6 + ';'
    arg7 = cur.execute(sql).fetchall()

## TODO def get_message_uuid(), pass it as a variable

    return render_template('book.html', email=arg0, hotel=arg1, agency=arg2,
                            name=arg3, nights=arg4, rcode=arg5,
                            activity=arg7)

@app.route('/request', methods=['POST'])
def request_tour():
    pass
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)
