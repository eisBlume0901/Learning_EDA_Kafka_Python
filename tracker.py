import json

from confluent_kafka import Consumer

# group.id - a unique string that identifies the consumer group this consumer belongs to
# auto.offset.reset -dictates what the consumer should do when it starts reading from a partition, but there is no valid
# previous offset found for its consumer group (for instance, if it is a completely new consumer group, or if the previously committed
# offset is for data that has already been deleted due to retention policies)
# - earliest - automatically reset the offset to the earliest offset
# - latest - automatically reset the offset to the latest offset
# - by_duration:<duration> - automatically reset the offset to a configured <duration> from the current timestamp
# none - throw exception o the consumer if no previous offset is found for the consumer's group
consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "order-tracker-group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)

# One consumer can subscribe to multiple topics
# .subscribe() - to receive messages from one or more topics
consumer.subscribe(["orders"])

print("Consumer is running and subscribed to orders topic")

try:
    # Check continuously if there is a new order from their subscribed orders topic
    while True:
        # .poll() - fetch data from the topics or partitions the consumer is subscribed to
        # 1.0 - timeout in seconds, will wait up to 1 second for new messages. If no messages are
        # immediately available, it will block (wait) for up to 1.0 seconds for new messages to arrive

        # Instead of Kafka using pushing new messages to the consumers, the consumers has the freedom
        # to pull messages at their own pace and processing capacity using .poll() method
        # Benefits: Load balancing, pausing, catching up, simple, reliable, scalable, controllable
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Producer encodes the message to what Kafka understands, Consumer decodes the message
        # into a string/
        value = msg.value().decode("utf-8")
        order = json.loads(value)
        print(f"Received order: {order.get("quantity")} x {order.get("item")} from {order.get("user")}")
except KeyboardInterrupt:
    print(f"\n Stopping consumer")
finally:
    # .close() - ensures that network connections and file handles are closed, offsets are committed, and the consumer's partition
    # assignments are revoked. Essential for properly releasing resources associated with a consumer instance.
    consumer.close()