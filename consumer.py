from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "my-topic-1",
    bootstrap_servers="localhost:19093",
    # join a consumer group for dynamic partition assignment and offset commits
    group_id="consumer-group-1",
    auto_offset_reset="earliest",
)
for msg in consumer:
    print(msg)
    print(msg.value.decode())
