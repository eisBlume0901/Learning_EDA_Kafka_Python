Docker commands
- docker-compose up - to start and run the Docker containers define din the docker-compose.yaml file

Kafka commands (exec mode)
- For more information about Kafka CLI - https://docs.confluent.io/kafka/operations-tools/kafka-tools.html
- Put docker exec -it kafka if using a command line server (remove them if using the Docker Desktop exec section)
- docker exec -it kafka-topics --list --botstrap-server localhost:9092 - to view the list of all available Kafka topics on the broker running at the localhost:9092
- docker exec -it kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning - to consume records from a topic. It reads data from Kafka topics and outputs it to a standard output