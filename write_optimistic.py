import hazelcast
import threading
import time


class Value:    
    def __init__(self, amount=0):
        self.amount = amount
    
    def __eq__(self, other):
        if not isinstance(other, Value):
            return False
        return self.amount == other.amount
    
    def __hash__(self):
        return hash(self.amount)
    
    def __repr__(self):
        return f"Value(amount={self.amount})"


def increment(client):
    map = client.get_map("test-map").blocking()
    for k in range(10_000):
        # if k % 10 == 0:
        #     print(f"At: {k}")
 
        while True:
            old_value = map.get("key")
            new_value = Value(old_value.amount)
            new_value.amount += 1

            if map.replace_if_same("key", old_value, new_value):
                break


if __name__ == "__main__":
    master_client = hazelcast.HazelcastClient(cluster_name="hello-world")
    master_map = master_client.get_map("test-map").blocking()
    master_map.put_if_absent("key", Value())

    client1 = hazelcast.HazelcastClient(cluster_name="hello-world")
    client2 = hazelcast.HazelcastClient(cluster_name="hello-world")
    client3 = hazelcast.HazelcastClient(cluster_name="hello-world")

    thread1 = threading.Thread(target=increment, args=(client1,))
    thread2 = threading.Thread(target=increment, args=(client2,))
    thread3 = threading.Thread(target=increment, args=(client3,))

    start_time = time.time()
    
    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    final_value = master_map.get("key")
    print(f"Final value of 'key': {final_value.amount}")
    print(f"Elapsed time (optimistic locking): {elapsed_time:.2f} seconds")

    master_client.shutdown()
    client1.shutdown()
    client2.shutdown()
    client3.shutdown()
