from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import sys
import time
import random
from datetime import datetime
import config

conf = config.get_config()


def insert_transaction(ct):

    # cord = random.randrange(2)

    if ct < 100:
        print ("Inserting debit transaction",ct)

        # debit transaction
        timestamp = datetime.now().isoformat(timespec='milliseconds')
        type = 0

        debit_amt = round(random.uniform(0.01, 9.99), 2)
        mdata = debit_merchants[random.randrange(len(debit_merchants))]
        merchant = mdata['merchant']
        description = mdata['description']
        debit_type = 0
        credit_amount = 0
        credit_type = 0                                                                                                                                                            #id, account_id,timestamp,type,debit_amount,debit_type,credit_amount,credit_type,merchant,description
    else:
        # credit transaction
        print ("Inserting credit transaction")
        timestamp = datetime.now().isoformat(timespec='milliseconds')

        type = 0
        #credit_amount = 7000
        credit_amount = round(random.uniform(300.00, 1500.00), 2)
        mdata = payment_cos[random.randrange(len(payment_cos))]
        merchant = mdata['payer']
        description = mdata['description']
        debit_type = 0
        debit_amt = 0
        credit_type = 0
        #print (f'INSERT INTO demo.transactions VALUES(\'{merchant}\')')

    id = session.execute("SELECT MAX(id) from transactions").one()[0]
    if (id is None):
        id = 1
    id = id + 1
    session.execute('INSERT INTO demo.transactions (id, account_id,date,type,debit_amount,debit_type,credit_amount,credit_type,merchant,description) VALUES (%s,%s,\'%s\',%s,%s,%s,%s,%s,\'%s\',\'%s\')' % (id, account_id, timestamp, type,debit_amt,debit_type,credit_amount,credit_type,merchant,description))
    print ('INSERT INTO demo.transactions (id, account_id,date,type,debit_amount,debit_type,credit_amount,credit_type,merchant,description) VALUES (%s,%s,\'%s\',%s,%s,%s,%s,%s,\'%s\',\'%s\')' % (id, account_id, timestamp, type,debit_amt,debit_type,credit_amount,credit_type,merchant,description))

if __name__ == "__main__":
    connt = []

    #contstruct a tuple of host/port
    for k,v in conf['DATABASE']['CONNECTIONS'].items():
        connt.append((v['host'],v['port']))

    # auth_provider = PlainTextAuthProvider(username='demo', password='Demo123!')
    # cluster = Cluster(auth_provider=auth_provider)
    auth_provider = PlainTextAuthProvider(username=conf['DATABASE']['USERNAME'], password=conf['DATABASE']['PASSWORD'])
    cluster = Cluster(connt,auth_provider=auth_provider)

    session = cluster.connect()
    account_id = 2 # hard coded account holder
    debit_merchants = [
        {'merchant':'Citco Gas','description':'Gas and sundries'},
        {'merchant':'Fresh Co','description':'Groceries'},
        {'merchant':'Friends Bar','description':'Food and drink'},
        {'merchant':'Table and Tap','description':'Food and drink'},
        {'merchant':'Amazon','description':'Online shopping'},
        {'merchant':'Walmart','description':'Retail'},
        {'merchant':'Home Depot','description':'Home improvement'},
        {'merchant':'Corner Bodega','description':'Deli and convenience'}
    ]
    payment_cos = [
        {'payer': 'Rockhill Systems','description':'Employee paycheck'},
        {'payer': 'Etsy','description':'Merchant Payer'},
        {'payer': 'Venmo','description':'Merchant Payer'}
    ]
    session.set_keyspace('demo')
    print ("Inserting transactions.")
    ct = 0
    while True:
        ct = ct + 1
        if ct > 100:
            ct = 0
        insert_transaction(ct)
        time.sleep(5)
