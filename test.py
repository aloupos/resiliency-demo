from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import config
import sys
import time
conf = config.get_config()

connt = []
#contstruct a tuple of host/port
for k,v in conf['DATABASE']['CONNECTIONS'].items():
    connt.append((v['host'],v['port']))

print (connt)
auth_provider = PlainTextAuthProvider(username=conf['DATABASE']['USERNAME'], password=conf['DATABASE']['PASSWORD'])
cluster = Cluster(connt,auth_provider=auth_provider)

try:
    session = cluster.connect()
except:
    pass
try:
    print(session.execute("SELECT release_version FROM system.local").one())
except:
    pass
while True:
    time.sleep(5)
#session.set_keyspace('demo')
#print(session.execute("SELECT * from customers").one())
