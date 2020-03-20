from kafka import KafkaConsumer
import traceback
import json
from elasticsearch import Elasticsearch, helpers

def getConfig():
    with open('./config.json') as config_file:
        config = json.load(config_file)
    return config

def get_client():
    config = getConfig()
    return Elasticsearch([config['es_port']])

def kafka_to_es(record):
    es_record = {'_index': 'test_log_snowplow',
                   '_type': '_doc',
                   '_id': record['etl_tstamp'] + '_' + record['event_name'],
                   '_source': record}
    return es_record

def push_kafka_to_es(es_records):
    es_client = get_client()
    helpers.bulk(es_client, es_records, chunk_size=500, request_timeout=20)

if __name__=="__main__":
    config = getConfig()
    
    kafka_consumer = KafkaConsumer(
        group_id=config['group_id'],
        bootstrap_servers=config['bootstrap_servers'],
        auto_offset_reset=config['offset'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    kafka_consumer.subscribe(['snowplow_json_event'])

    es_records = []

    while True:
        message = next(kafka_consumer)
        if message is None: continue
        json_event = message.value
        print(json_event)
        try:
            es_records.append(kafka_to_es(json_event))
<<<<<<< HEAD
            if(len(es_records) == 100):
=======
            if(len(es_records) == 1 ):
>>>>>>> a92cf986e77af24de34bca471bcb2524309c3ca5
                push_kafka_to_es(es_records)
                es_records.clear()
        except Exception as e:
            traceback.print_exc()
