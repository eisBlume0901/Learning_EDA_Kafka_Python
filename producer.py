import json
import uuid
from confluent_kafka import Producer

# bootstrap.servers - provides the initial hosts that act as a starting
# point for Kafka client to discover the full set of alive servers in the cluster
producer_config = {
    "bootstrap.servers": "localhost:9092"
}

producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered successfully: {msg.value().decode("utf-8")}")
        print(dir(msg)) # to review the key fields of the message
        print(f"Delivered to {msg.topic()} : partition: {msg.partition()} at offset: {msg.offset()}")

order = {
    "order_id": str(uuid.uuid4()),
    "user": "eisBlume0901",
    "item": "Mary Jane pumps",
    "quantity": 1,
}

value = json.dumps(order).encode("utf-8") # Kafka understands binary codes not human-level descriptions

# Created a topic named "orders"
producer.produce(
    topic="orders",
    value=value,
    callback=delivery_report
)

# flush() - waits for all buffered messages in the producer's internal queue to be
# delivered to the Kafka broker and acknowledged before returning. This ensures that all messages have been sent before the program exits.
producer.flush()

