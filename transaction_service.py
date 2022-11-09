from flask import Flask
from flask import request
from flask import Response
import logging
import os
import json
import collections
from db_cassandra import session
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
import sys
import time
import random
import json
from decimal import *
from datetime import datetime
logging.getLogger('flask_cors').level = logging.DEBUG
import config

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

@app.after_request
def response_processor(response):
    # Prepare all the local variables you need since the request context
    # will be gone in the callback function

    @response.call_on_close
    def process_after_request():
        # Do whatever is necessary here
        print ("after")
        print (response.status)
        print (type(response.status))
        if (response.status == '500 INTERNAL SERVER ERROR'):
            print ("The server encountered an error, most likely due to the availability of dbs.  Exiting.")
            os._exit(0)
        pass

    return response

@app.route("/")
def hello():
    return "ok"

@app.route("/transactions")
def transactions():
    aid = request.args.get('account_id')
    if (aid is None):
        q = session.execute('select * from transactions where account_id = %s order by id desc limit 50' % account_id).all()
    else:
        q = session.execute('select * from transactions where account_id = %s order by id desc limit 50' % aid).all()
    return (q)

@app.route("/balance")
def balance():
    # try:
    q = session.execute('select id,account_type_id from account where customer_id = 2 ALLOW FILTERING')
    # except Exception as e:
    #     print (e)
    #     return Response("{}", status=500, mimetype='application/json')

    # print (q[0])
    res = []
    for row in q:
        b = session.execute ('select account_id,sum(credit_amount) as credits, sum(debit_amount) as debits from demo.transactions where account_id = %s;' % row['id']).all()
        b[0].update (session.execute ('select product_name from demo.account_type where id = %s' % row['account_type_id']).all()[0])
        bal = (b[0]['credits'] - b[0]['debits'])
        b[0].update (collections.OrderedDict([('balance',bal)]))
        res.append (b[0])
    return (res)



if __name__ == "__main__":
    session = session.session()
    session.set_keyspace('demo')
    account_id = 2
    print ("Starting transaction service.")
    app.run(host='0.0.0.0')
