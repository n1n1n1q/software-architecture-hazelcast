import hazelcast
import threading

def produce(client):
    queue = client.get_queue("bounded-queue").blocking()
    for i in range(1, 101):
        queue.put(i)
        print(f"Put {i}")
    queue.put(-1)
    print(f"Put poison pill")

if __name__ == "__main__":
    client = hazelcast.HazelcastClient(cluster_name="hello-world")
    
    thread_producer= threading.Thread(target=produce, args=(client,))
    thread_producer.start()
    thread_producer.join()
    client.shutdown()