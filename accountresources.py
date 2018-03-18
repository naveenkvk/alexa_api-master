
from models import Account
from db import session

from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with

account_fields = {
    'account_id': fields.Integer,
    'account_name': fields.String,
    'account_type': fields.String,
    'account_status': fields.String,
    'uri': fields.Url('account', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('account_name', type=str)

class AccountResource(Resource):
    @marshal_with(account_fields)
    def get(self, account_name):
        account = session.query(Account).filter(Account.account_name == account_name).first()
        if not account:
            abort(404, message="Account {} doesn't exist".format(account_name))
        return account

    def delete(self, account_name):
        account = session.query(Account).filter(Account.account_name == account_name).first()
        if not account:
            abort(404, message="Account {} doesn't exist".format(account_name))
        session.delete(account)
        session.commit()
        return {}, 204

    @marshal_with(account_fields)
    def put(self, account_name):
        parsed_args = parser.parse_args()
        account = session.query(Account).filter(Account.account_name == account_name).first()
        account.task = parsed_args['account_name']
        session.add(account)
        session.commit()
        return account, 201


class AccountListResource(Resource):
    @marshal_with(account_fields)
    def get(self):
        account = session.query(Account).all()
        return account

    @marshal_with(account_fields)
    def post(self):
        parsed_args = parser.parse_args()
        account = Account(task=parsed_args['account_name'])
        session.add(account)
        session.commit()
        return account, 201
