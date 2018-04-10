
from models import ServiceNow
from db import session

from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from sqlalchemy import func

ticket_fields = {
    'ticket_id': fields.Integer,
    'ticket_category': fields.String,
    'ticket_status': fields.String,
    'ticket_description': fields.String,
    'ticket_comment' : fields.String,
    'create_date' : fields.DateTime,
    'priotity' : fields.String,
    'assigned_to' : fields.String,
    'assignment_group' : fields.String,
    'requestor' : fields.String,
    'uri': fields.Url('ticket', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('ticket_category', type=str)
parser.add_argument('priotity', type=str)
parser.add_argument('ticket_description', type=str)

class TicketToResource(Resource):
    @marshal_with(ticket_fields)
    def get(self, assigned_to):
        ticket = session.query(ServiceNow).filter(func.lower(ServiceNow.assigned_to) == func.lower(assigned_to)).all()
        if not ticket:
            abort(404, message="Ticket {} doesn't exist".format(assigned_to))
        return ticket

    def delete(self, assigned_to):
        ticket = session.query(ServiceNow).filter(func.lower(ServiceNow.assigned_to) == func.lower(assigned_to)).all()
        if not ticket:
            abort(404, message="Ticket {} doesn't exist".format(assigned_to))
        session.delete(ticket)
        session.commit()
        return {}, 204

    @marshal_with(ticket_fields)
    def put(self, assigned_to):
        parsed_args = parser.parse_args()
        ticket = session.query(ServiceNow).filter(func.lower(ServiceNow.assigned_to) == func.lower(assigned_to)).all()
        ticket.task = parsed_args['assigned_to']
        session.add(ticket)
        session.commit()
        return ticket, 201

class TicketByResource(Resource):
    @marshal_with(ticket_fields)
    def get(self, requestor):
        ticket = session.query(ServiceNow).filter(func.lower(ServiceNow.requestor) == func.lower(requestor)).all()
        if not ticket:
            abort(404, message="Ticket {} doesn't exist".format(requestor))
        return ticket

    def delete(self, requestor):
        ticket = session.query(ServiceNow).filter(func.lower(ServiceNow.requestor) == func.lower(requestor)).all()
        if not ticket:
            abort(404, message="ServiceNow {} doesn't exist".format(requestor))
        session.delete(ticket)
        session.commit()
        return {}, 204

    @marshal_with(ticket_fields)
    def put(self, requestor):
        parsed_args = parser.parse_args()
        ticket = session.query(ServiceNow).filter(func.lower(ServiceNow.requestor) == func.lower(requestor)).first()
        ticket.task = parsed_args['requestor']
        session.add(ticket)
        session.commit()
        return ticket, 201
    
    @marshal_with(ticket_fields)
    def post(self,requestor): 
        parsed_args = parser.parse_args()
        ticket_category=parsed_args['ticket_category']
        priotity=parsed_args['priotity']
        ticket_description=parsed_args['ticket_description']
        ticket = ServiceNow(ticket_id= 100, ticket_status='Created',ticket_category=ticket_category, create_date='1-JAN-2018',
                            assigned_to='Kevin',assignment_group="Application Support",priotity=priotity, requestor=requestor,
                            ticket_description=ticket_description)
        session.add(ticket)
        session.commit()
        return ticket, 201

class TicketListResource(Resource):
    @marshal_with(ticket_fields) 
    def get(self):
        ticket = session.query(ServiceNow).all()
        return ticket
    
    @marshal_with(ticket_fields)
    def post(self):
        parsed_args = parser.parse_args()
        category=parsed_args['ticket_category']
        priority=parsed_args['priotity']
        description=parsed_args['ticket_description']
        ticket = ServiceNow(ticket_id= 100, ticket_status='Created',ticket_category=category, create_date='1-JAN-2018',
                            assigned_to='Kevin',assignment_group="Application Support",priotity=priority, requestor="John",
                            ticket_description=description)
        session.add(ticket)
        session.commit()
        return ticket, 201
    
