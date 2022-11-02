from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import AddressTranslator
from cassandra.query import ordered_dict_factory

import config
import sys
import time
conf = config.get_config()
connt = []
for k,v in conf['DATABASE']['CONNECTIONS'].items():
    connt.append((v['host'],v['port']))



class K8SAddressTranslator(AddressTranslator):

    def translate(self, addr):

        print('in translate(self, addr) method', type(addr), addr)
        trans_addr = connt[0]
        return trans_addr


class session:
    def session():
        k8s_translator = K8SAddressTranslator()
        auth_provider = PlainTextAuthProvider(username=conf['DATABASE']['USERNAME'], password=conf['DATABASE']['PASSWORD'])
        cluster = Cluster(connt,auth_provider=auth_provider,address_translator = k8s_translator)
        try:
            session = cluster.connect()
        except Exception as e:
            print(e)
            raise ValueError('No databases available.')
        session.row_factory = ordered_dict_factory
        return (session)
