import hazelcast
import threading

def consume(client, client_id):
    queue = client.get_queue("bounded-queue").blocking()
    while True:
        value = queue.take()
        if value == -1:
            queue.put(-1)
            print("Poison pill taken")
            break
        print(f"Read {value}, client {client_id}")

def produce(client):
    queue = client.get_queue("bounded-queue").blocking()
    for i in range(1, 101):
        queue.put(i)
        print(f"Put {i}")
    queue.put(-1)
    print(f"Put poison pill")

if __name__ == "__main__":
    client1 = hazelcast.HazelcastClient(cluster_name="hello-world")
    client2 = hazelcast.HazelcastClient(cluster_name="hello-world")
    client3 = hazelcast.HazelcastClient(cluster_name="hello-world")

    thread_producer= threading.Thread(target=produce, args=(client1,))
    thread_consumer1 = threading.Thread(target=consume, args=(client2, 2, ))
    thread_consumer2 = threading.Thread(target=consume, args=(client3, 3, ))

    thread_producer.start()
    thread_consumer1.start()
    thread_consumer2.start()

    thread_producer.join()
    thread_consumer1.join()
    thread_consumer2.join()

    client1.shutdown()
    client2.shutdown()
    client3.shutdown()
