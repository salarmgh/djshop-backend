from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['elasticsearch'])
