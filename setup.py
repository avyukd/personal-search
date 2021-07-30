from elasticsearch import Elasticsearch, helpers
import configparser

config = configparser.ConfigParser()
config.read('example.ini')

es = Elasticsearch(
    cloud_id=config['DEFAULT']['cloud_id'],
    api_key=(config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
)

print(es.info())