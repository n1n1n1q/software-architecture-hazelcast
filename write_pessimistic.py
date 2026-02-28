import hazelcast
import threading
import time

def increment(client):
    map = client.get_map("test-map").blocking()
    for k in range(10_000):
        if k % 10 == 0:
            print(f"Client {client} at {k}")
        map.lock("key")
        try:
            value = map.get("key")
            value += 1
            map.put("key", value)
        finally:
            map.unlock("key")

if __name__ == "__main__":
    master_client = hazelcast.HazelcastClient(cluster_name="hello-world")
    master_map = master_client.get_map("test-map").blocking()
    master_map.put_if_absent("key", 0)

    client1 = hazelcast.HazelcastClient(cluster_name="hello-world")
    client2 = hazelcast.HazelcastClient(cluster_name="hello-world")
    client3 = hazelcast.HazelcastClient(cluster_name="hello-world")

    thread1 = threading.Thread(target=increment, args=(client1,))
    thread2 = threading.Thread(target=increment, args=(client2,))
    thread3 = threading.Thread(target=increment, args=(client3,))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    final_value = master_map.get("key")
    print(f"Final value of 'key': {final_value}")

    master_client.shutdown()
    client1.shutdown()
    client2.shutdown()
    client3.shutdown()
