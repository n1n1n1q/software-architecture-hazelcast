import hazelcast
import time

if __name__=="__main__":
    client = hazelcast.HazelcastClient(cluster_name="hello-world")
    print("connected")
    dist_map = client.get_map("test-map").blocking()

    for i in range(1001):
        start_time = time.time()
        dist_map.put(i, f"nymber {i}")
        print(time.time() - start_time)

    for i in range(1001):
        print(dist_map.get(i))
    print("bebra")