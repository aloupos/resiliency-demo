from flask import Flask
from flask import request
import logging
import json
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
from cassandra.cluster import Cluster
from cassandra.query import ordered_dict_factory
from cassandra.auth import PlainTextAuthProvider
import sys
import time
import random
import json
from decimal import *
from datetime import datetime
logging.getLogger('flask_cors').level = logging.DEBUG


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)


@app.route("/")
def hello():
    return "Hello from Python!"

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
    q = session.execute('select id,account_type_id from account where customer_id = 2 ALLOW FILTERING')
    # print (q[0])
    res = []
    for row in q:
        b = session.execute ('select account_id,sum(credit_amount) as credits, sum(debit_amount) as debits, sum(credit_amount) - sum(debit_amount) as balance from demo.transactions where account_id = %s;' % row['id']).all()
        b[0].update (session.execute ('select product_name from demo.account_type where id = %s' % row['account_type_id']).all()[0])
        res.append (b[0])
        # res.append(json.dumps(b[0], indent=4, cls=DecimalEncoder))
        print (res)
    return (res)



if __name__ == "__main__":
    auth_provider = PlainTextAuthProvider(username='demo', password='Demo123!')
    cluster = Cluster(auth_provider=auth_provider)
    session = cluster.connect()
    session.row_factory = ordered_dict_factory
    session.set_keyspace('demo')
    account_id = 2
    app.run(host='0.0.0.0')
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    # # hard coded account_id
