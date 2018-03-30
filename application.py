#!/usr/bin/env python

from flask import Flask
from flask.ext.restful import Api

application = app = Flask(__name__)
api = Api(app)

from resources import TodoListResource
from resources import TodoResource

from accountresources import AccountResource
from accountresources import AccountListResource

from transactionresources import TransactionResource
from transactionresources import TransactionListResource


api.add_resource(TodoListResource, '/todos', endpoint='todos')
api.add_resource(TodoResource, '/todos/<string:id>', endpoint='todo')

api.add_resource(AccountListResource, '/account', endpoint='accounts')
api.add_resource(AccountResource, '/account/<string:account_name>', endpoint='account')

api.add_resource(TransactionListResource, '/transaction', endpoint='transactions')
api.add_resource(TransactionResource, '/transaction/<string:transaction_type>', endpoint='transaction')

api.add_resource(TicketListResource, '/ticket', endpoint='tickets')
api.add_resource(TicketToResource, '/ticket/<string:assigned_to>', endpoint='assigned_to')
api.add_resource(TicketByResource, '/ticket/<string:requestor>', endpoint='requestor')


if __name__ == '__main__':
    app.run(debug=True)
