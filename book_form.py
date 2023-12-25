#!/usr/bin/env python
# coding: utf-8

## Copyright Humberto Yances, author. All rights reserved.

from flask import Flask
from flask import request
from flask import render_template
import flask_resize
import os
from database import engine
from sqlalchemy import text


host = '0.0.0.0'
port = '9090'

app = Flask('book_form')
root = os.path.join(app.root_path)
app.config['RESIZE_URL'] = 'http://' + host + ':' + port + '/static'
app.config['RESIZE_ROOT'] = root + '/static'
resize = flask_resize.Resize(app)


def load_tours_from_db(tour_id):
    with engine.connect() as conn:
        result = conn.execute(text("select * from tours where id = " + tour_id))
        tours = []
        for row in result.all():
            tours.append(dict(row._mapping))
        return tours


@app.route('/book', methods=['GET'])
def book_tour():

    email = request.args.get('em', 'best@experience.com')
    hotel = request.args.get('ht', 'sublime exprience')
    agency = request.args.get('ag', 'best experince in the world')
    guest_name = request.args.get('nm', 'Fulano')
    nights = request.args.get('ng', '1')
    rcode = request.args.get('rc', '1')
    activity_id = request.args.get('ac', '3')
    activity = load_tours_from_db(activity_id)

    return render_template('book.html', email=email, hotel=hotel, agency=agency,
                            name=guest_name, nights=nights, rcode=rcode,
                            activity=activity)

@app.route('/request_book', methods=['POST'])
def request_tour():
    pass
 

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)

