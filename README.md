# Kafka kraft studies

In `docker-compose.yml`, a three-node Kafka cluster is created. It uses KRaft mode instead of Zookeepers, because I wanted to get to know KRaft.  
The nodes communicate with each other through the network created by docker compose.

There are very simple Python producer and consumer that you can test the cluster with. They use both kafka-python and confluent-kafka to try them out.

[AKHQ](https://akhq.io/) is also running with a super basic config and accessible at [localhost:8080](localhost:8080). You can view the cluster status from there. 

Notes:
  - `KAFKA_CFG_LISTENERS` is the address that the broker itself listens to. In e.g. kafka1, the broker listens to port 9092.
  - `KAFKA_CFG_ADVERTISED_LISTENERS` is the host:port combo that the broker tells others to connect to. in e.g. kafka2, the broker tells to use kafka2:9095 for controller traffic, and the broker itself listens to port 9094 of the container.
  - A node with a dedicated controller property or dual property must not advertise its controller listener.
  - A bare broker node cannot be included in the quorum voters (`KAFKA_CFG_CONTROLLER_QUORUM_VOTERS`)
  - Inside a docker network, containers are accessible by their internal port, not the host port (so second in the ports section, not first) 
    - [confluent documentation](https://docs.confluent.io/platform/7.5/installation/configuration/broker-configs.html#process-roles) says that the dual role of a server (broker, controller) is an early access feature and does not support production workloads. This testing used that mode on all three nodes.
      - This means that until the dual mode is ready for production use, the kraft mode does not actually lessen the amount of nodes needed for a stable and failure-tolerant cluster. As of January 21, 2024 I did not find any roadmap for production use, or even mentions of whether that 'not suitable for production' info is stale or not.
  - Topics are currently created on the fly, when messages are produced to a new topic
  - The `data` folder and subfolders need to belong to user `1001`, since the Bitnami Kafka container is a non-root container. See [here](https://docs.bitnami.com/tutorials/why-non-root-containers-are-important-for-security) for more details.

Future work:
  - Repeat the process in a cloud platform with separate machines
      - Create proper networking rules for the cluster
      - Add more nodes and set the `KAFKA_CFG_PROCESS_ROLES` to be only broker or a controller
      - Add authentication and encryption

