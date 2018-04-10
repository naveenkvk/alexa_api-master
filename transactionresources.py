
from models import Transaction
from db import session

from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from sqlalchemy import func

transaction_fields = {
    'transaction_id': fields.Integer,
    'instrument_name': fields.String,
    'transaction_type': fields.String,
    'transaction_dt': fields.DateTime,
    'net_transaction_amt' : fields.Integer,
    'transaction_qty' : fields.Integer,
    'account_id' : fields.Integer,
    'uri': fields.Url('transaction', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('transaction_type', type=str)
parser.add_argument('account_id', type=str)

class TransactionResource(Resource):
    @marshal_with(transaction_fields)
    def get(self, transaction_type):
        transaction = session.query(Transaction).filter(func.lower(Transaction.transaction_type) == func.lower(transaction_type)).all()
        if not transaction:
            abort(404, message="Transaction {} doesn't exist".format(transaction_type))
        return transaction

    def delete(self, transaction_type):
        transaction = session.query(Transaction).filter(func.lower(Transaction.transaction_type) == func.lower(transaction_type)).first()
        if not transaction:
            abort(404, message="Transaction {} doesn't exist".format(transaction_type))
        session.delete(transaction)
        session.commit()
        return {}, 204

    @marshal_with(transaction_fields)
    def put(self, transaction_type):
        parsed_args = parser.parse_args()
        transaction = session.query(Transaction).filter(func.lower(Transaction.transaction_type) == func.lower(transaction_type)).first()
        transaction.transaction_type = parsed_args['transaction_type']
        session.add(transaction)
        session.commit()
        return transaction, 201

    @marshal_with(transaction_fields)
    def post(self,transaction_type):
        parsed_args = parser.parse_args()
        account_id=parsed_args['account_id']
        
        if account_id != "0":
            transaction = session.query(Transaction).filter(func.lower(Transaction.transaction_type) == func.lower(transaction_type),
                                                           func.lower(Transaction.account_id) == func.lower(account_id)).all()
        else:
            transaction = session.query(Transaction).filter(func.lower(Transaction.transaction_type) == func.lower(transaction_type)).all()
        if not transaction:
            abort(404, message="Transaction {} doesn't exist".format(transaction_type))
        return transaction, 201


class TransactionListResource(Resource):
    @marshal_with(transaction_fields)
    def get(self):
        transaction = session.query(Transaction).all()
        return transaction

    @marshal_with(transaction_fields)
    def post(self):
        parsed_args = parser.parse_args()
        transaction = Transaction(transaction_type=parsed_args['transaction_type'])
        session.add(transaction)
        session.commit()
        return transaction, 201
