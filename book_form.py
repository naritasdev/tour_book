#!/usr/bin/env python
# coding: utf-8

## Copyright Humberto Yances, author. All rights reserved.

from flask import Flask
from flask import request
from flask import render_template
import flask_resize
import os
from database import engine
from mailer import send_email
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
    """

    Parameters
    ----------
    tour_id :
        

    Returns
    -------

    """
    with engine.connect() as conn:
        result = conn.execute(text("select * from tours where id = " + tour_id))
        tours = []
        for row in result.all():
            tours.append(dict(row._mapping))
        return tours

def load_request_from_db(request_id): # or request_name
    """

    Parameters
    ----------
    request_id :
        

    Returns
    -------

    """
    with engine.connect() as conn:
        result = conn.execute(text("select * from request where id = " + request_id))
        request = []
        for row in result.all():
            request.append(dict(row._mapping))
        return request

def add_request_from_db(data): 
    """

    Parameters
    ----------
    data :
        

    Returns
    -------

    """
    with engine.connect() as conn:
        result = text("insert into request (name,email,activity,date,requests,hotel,agency,category,description) values (:nombreName, :email, :actividadTour, :fechaDate, :solicitudesRequests), :hotel, :agency, :category, :description" )
        conn.execute(statement=result, parameters=dict( nombreName=data['nombreName'],
                     email=data['email'],
                     actividadTour=data['actividadTour'],
                     fechaDate=data['fechaDate'],
                     solicitudesRequests=data['solicitudesRequests'],
                     hotel=data['hotel'],
                     agency=data['agency'],
                     category=data['category'],
                     description=data['description']))
        


@app.route('/', methods=['GET'])
def book_tour():
    """ """

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
    """ 
    A book request asked by hotel guest.  Registered in the database and send 
      emails to each party involved: guest, hotel, agency and tech provider. 

    """

    guest_name = request.form['nombreName']
    email = request.form['email']
    #activity_id = '3' 
    #activity_name = request.form['actividadTour']
    #activity = load_request_from_db(activity_id or activity_name)
    hotel = request.form['hotel']
    agency = request.form['agency']
    activity = request.form['actividadTour']
    category = request.form['category']
    fechaDate = request.form['fechaDate']
    solicitudesRequests = request.form['solicitudesRequests']
    category = request.form['category']
    description = request.form['description']
    data = request.form
    # save request to database
    add_request_from_db(data)
    # send request copy by email
    htmlContent = "<!DOCTYPE html> <html> <body> <h1> {{guest_name}} ha realizado \
                   una solicitud de reserva. </h1> <p>Estos son los datos almacenados: \
                   </p><ul><li>Nombre/Name: {{guest_name}}.</li><li>Email: {{email}}. \
                   </li><li>Hotel: {{hotel}}.</li> \
                   </li><li>Agencia/Agency: {{agency}}.</li> \
                   </li><li>Actividad/Activity: {{actividadTour}}.</li> \
                   </li><li>Categoría/Category: {{category}}.</li> \
                   </li><li>Descripción/Description: {{description}}.</li> \
                   <li>Fecha/Date: {{fechaDate}}.</li><li>Solicitudes/Requests: \
                   {{solicitudesRequests}}.</li></ul> </body> </html>"
    textContent = "Han realizado una solicitud de reserva."
    subject = "Confirmación de solicitud de reserva."
    tags='["tourBookRequest"]'

    mailer_response = send_email(
        sender=('hotel', 'info@naritas.co'),
               reply=('noreply', 'noreply@reply.hotel.com'),
               to=[(guest_name, email)],
               cc=[('hotel', 'test1@naritas.co'), ('agency', 'test2@naritas.co')],
               bcc=[('techProvider', 'soporte@naritas.co'), 
                    ('sales', 'sales@naritas.co')],
               htmlContent=htmlContent,
               textContent=textContent,
               subject=subject,
               tags=tags
              )

    return render_template('confirmation.html', name=guest_name, email=email, 
                           activity=activity, 
                           fechaDate=fechaDate, solicitudesRequests=solicitudesRequests, mailer_response=mailer_response, hotel=hotel, agency=agency, category=category, description=description) 

 

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)

