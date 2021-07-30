#possibly want filenames to be hashed for additional security
#only single client can unhash so that noobdy else can get a unique filepath

from elasticsearch import Elasticsearch, helpers
import configparser


def start_es():
    config = configparser.ConfigParser()
    config.read('example.ini')

    es = Elasticsearch(
        cloud_id=config['DEFAULT']['cloud_id'],
        api_key=(config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
    )
    return es
