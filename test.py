from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import AddressTranslator
import config
import sys
import time
conf = config.get_config()

connt = []
#contstruct a tuple of host/port
for k,v in conf['DATABASE']['CONNECTIONS'].items():
    connt.append((v['host'],v['port']))

#print (connt)
# code from Rajesh
class K8SAddressTranslator(AddressTranslator):

    def translate(self, addr):

        print('in translate(self, addr) method', type(addr), addr)
        trans_addr = connt[0]
        return trans_addr
################################################################################


k8s_translator = K8SAddressTranslator()




auth_provider = PlainTextAuthProvider(username=conf['DATABASE']['USERNAME'], password=conf['DATABASE']['PASSWORD'])
cluster = Cluster(connt,auth_provider=auth_provider,address_translator = k8s_translator)

try:
    session = cluster.connect()
except Exception as e:
    print(e)
    pass
try:
    #print(session.execute("SELECT release_version FROM system.local").one())
    print(session.execute("SELECT data_center, rack, host_id, release_version FROM system.local").all())
except:
    pass
while True:
    time.sleep(5)
    #print (cluster.contact_points)
    print (session.execute("SELECT sum(credit_amount) from demo.transactions").one())
    print(session.execute("SELECT data_center, rack, host_id, release_version FROM system.local").all())
    #print(session.execute("SELECT release_version FROM system.local").one())
#session.set_keyspace('demo')
#print(session.execute("SELECT * from customers").one())
