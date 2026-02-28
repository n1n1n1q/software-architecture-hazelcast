import hazelcast

if __name__ == "__main__":
    client = hazelcast.HazelcastClient(cluster_name="hello-world")

    map = client.get_map("test-map")
    map.clear().result()