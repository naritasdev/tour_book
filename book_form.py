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
from flask import url_for


host = '0.0.0.0'
port = '9090'

app = Flask(__name__)
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

def load_request_from_db(request_id): # or request_name
    with engine.connect() as conn:
        result = conn.execute(text("select * from request where id = " + request_id))
        request = []
        for row in result.all():
            request.append(dict(row._mapping))
        return request

def add_request_from_db(request_name, request_email, request_date, request_requests): 
    with engine.connect() as conn:
        result = text("insert into request (name,email,date,requests) values (?, ?, ?, ?)" )
        conn.execute(result,
                     "+request_name+",
                     "+request_email+",
                     "+request_date+",
                     "request_requests")


@app.route('/', methods=['GET'])
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
    
    

    guest_name = request.form['nombreName']
    email = request.form['email']
    #activity_id = '3' 
    #activity_name = request.form['actividadTour']
    #activity = load_request_from_db(activity_id or activity_name)
    
    fechaDate = request.form['fechaDate']
    solicitudesRequests = request.form['solicitudesRequests']
    add_request_from_db(guest_name,email,fechaDate,solicitudesRequests)    
    
    return render_template('confirmation.html', name=guest_name, email=email, 
                           #activity=activity, 
                           fechaDate=fechaDate, solicitudesRequests=solicitudesRequests) 



 

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)

