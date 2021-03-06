from confluent_kafka import Producer, Consumer, KafkaError
import snowplow_analytics_sdk.event_transformer
import snowplow_analytics_sdk.snowplow_event_transformation_exception
import json

def getConfig():
    with open('./config.json') as config_file:
        config = json.load(config_file)
    return config

if __name__=="__main__":

    config = getConfig()

    kafka_consumer = Consumer({
        'bootstrap.servers': config['bootstrap_servers'],
        'group.id': config['group_id'],
        'default.topic.config': {
            'auto.offset.reset': config['offset']
        }
    })

    kafka_producer = Producer({
<<<<<<< HEAD
        'bootstrap.servers': config['bootstrap_servers']
=======
        'bootstrap.servers': config['bootstrap_servers_producer']
>>>>>>> a92cf986e77af24de34bca471bcb2524309c3ca5
        # 'bootstrap.servers': ["10.10.137.42:6667", "10.10.137.43:6667"]
    })
    kafka_consumer.subscribe(['snowplow_enriched_good'])

    while True:
        msg = kafka_consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF: continue
            else:
                print("kafka error: " + msg.error())
                break

        event = msg.value().decode('utf-8')
        # print(event)
        try:
            json_data = snowplow_analytics_sdk.event_transformer.transform(event)
            kafka_producer.poll(0)
            kafka_producer.produce('snowplow_json_event', json.dumps(json_data).encode('utf-8'))
            kafka_producer.flush()

        except snowplow_analytics_sdk.snowplow_event_transformation_exception.SnowplowEventTransformationException as e:
            for error_message in e.error_messages:
                print("kafka error: " + error_message)