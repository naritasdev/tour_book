#!/usr/bin/env python
# coding: utf-8

## Copyright Humberto Yances, author. All rights reserved.

from flask import Flask
from flask import request,requests
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

def add_request_from_db(data): 
    with engine.connect() as conn:
        result = text("insert into request (name,email,date,requests) values (:nombreName, :email, :fechaDate, :solicitudesRequests)" )
        conn.execute(statement=result, parameters=dict( nombreName=data['nombreName'],
                     email=data['email'],
                     fechaDate=data['fechaDate'],
                     solicitudesRequests=data['solicitudesRequests']))
        


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
    data = request.form
    add_request_from_db(data)
    url= "https://api.brevo.com/v3/smtp/email"
    payload = {
    "sender": {
        "name": "Mary from MyShop",
        "email": "hyances@naritas.co"
    },
    "replyTo": {
        "email": email,
        "name": "Guest"
    },
    "to": [
        {
            "email": "daniel.pajaro98@gmail.com",
            "name": "sublime exprience hotel"
        },
        {
            "email": "hyances@naritas.co",
            "name": "best experince in the world agency"
        }
    ],
    "bcc": [
        {
            "email": "hyances@naritas.co",
            "name": "Naritas"
        }
    ],
    "cc": [
        {
            "email": "daniel.pajaro98@yahoo.com",
            "name": "Tour book & management"
        }
    ],
    "htmlContent": "<!DOCTYPE html> <html> <body> <h1> {{guest_name}} ha realizado una solicitud de reserva. </h1> <p>Estos son los datos almacenados:</p><ul><li>Nombre/Name: {{guest_name}}.</li><li>Email: {{email}}.</li>li>Fecha/Date: {{fechaDate}}.</li><li>Solicitudes/Requests: {{solicitudesRequests}}.</li></ul> </body> </html>",
    "textContent": "Han realizado una solicitud de reserva.",
    "subject": "Confirmación de solicitud de reserva.",
    "tags": ["tourBookRequest"]
    }    
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": "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"
    }
    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


    return render_template('confirmation.html', name=guest_name, email=email, 
                           #activity=activity, 
                           fechaDate=fechaDate, solicitudesRequests=solicitudesRequests) 



 

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)

