import random
import math

class Node:
    def __init__(self, node_id, x, y, r, e, p):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.r = r  # Radio range
        self.e = e  # Energy level
        self.p = p  # Processing power
        self.cluster = None  # Initially, the node is not part of any cluster

    def calculate_f(self):
        # F = 0.4 * R + 0.4 * E + 0.2 * P
        return 0.4 * self.r + 0.4 * self.e + 0.2 * self.p

    def distance_to(self, other_node):
        # Calculate Euclidean distance to another node
        return math.sqrt((self.x - other_node.x)**2 + (self.y - other_node.y)**2)

class Cluster:
    def __init__(self, cluster_id, x, y, size):
        self.cluster_id = cluster_id
        self.x = x
        self.y = y
        self.size = size
        self.nodes = []  # List to store nodes belonging to the cluster
        self.clusterhead = None  # Initially, no clusterhead is elected

    def add_node(self, node):
        # Add a node to the cluster and set its cluster reference
        if node not in self.nodes:
            self.nodes.append(node)
            node.cluster = self

    def elect_clusterhead(self):
        if not self.nodes:
            return None

        # Find the node with the highest F value
        max_f = float('-inf')
        candidates = []

        for node in self.nodes:
            f = node.calculate_f()
            if f > max_f:
                max_f = f
                candidates = [node]
            elif f == max_f:
                candidates.append(node)

        # If there's a tie, choose the node closest to the cluster center
        if len(candidates) > 1:
            center_x = self.x + self.size / 2
            center_y = self.y + self.size / 2
            self.clusterhead = min(candidates, key=lambda n: (n.x - center_x)**2 + (n.y - center_y)**2)
        else:
            self.clusterhead = candidates[0]

        return self.clusterhead

class WSN:
    def __init__(self, width, height, cluster_size):
        self.width = width
        self.height = height
        self.cluster_size = cluster_size
        self.nodes = []  # All nodes in the network
        self.clusters = []  # All clusters in the network
        self._initialize_clusters()

    def _initialize_clusters(self):
        cluster_id = 0
        for x in range(0, self.width, self.cluster_size):
            for y in range(0, self.height, self.cluster_size):
                self.clusters.append(Cluster(cluster_id, x, y, self.cluster_size))
                cluster_id += 1

    def add_node(self, node):
        # Add the node and assign it to the correct cluster
        self.nodes.append(node)
        cluster_x = int(node.x // self.cluster_size)
        cluster_y = int(node.y // self.cluster_size)
        cluster_index = cluster_y * (self.width // self.cluster_size) + cluster_x
        if 0 <= cluster_index < len(self.clusters):
            self.clusters[cluster_index].add_node(node)
        else:
            print(f"Error: Node {node.node_id} with coordinates ({node.x}, {node.y}) assigned to invalid cluster index {cluster_index}")

    def elect_clusterheads(self):
        # Elect clusterheads for each cluster
        for cluster in self.clusters:
            cluster.elect_clusterhead()

    def route(self, source_id, dest_id):
        source = next((node for node in self.nodes if node.node_id == source_id), None)
        dest = next((node for node in self.nodes if node.node_id == dest_id), None)

        if not source or not dest:
            print(f"Source or destination node not found. Source ID: {source_id}, Destination ID: {dest_id}")
            return None

        path = [source]
        current = source

        while current != dest:
            neighbors = [node for node in self.nodes if node != current and current.distance_to(node) <= current.r]
            if not neighbors:
                print(f"No neighbors found for node {current.node_id} within radio range.")
                return None  # No route found

            next_hop = min(neighbors, key=lambda n: n.distance_to(dest))
            if next_hop in path:
                print(f"Loop detected. Node {next_hop.node_id} is already in the path.")
                return None  # Prevent loops
            path.append(next_hop)
            current = next_hop

        return path

def generate_random_node(node_id):
    return Node(
        node_id + 1,  # Start IDs from 1
        random.uniform(0, 20),
        random.uniform(0, 20),
        random.randint(1, 8),
        random.randint(1, 100),
        random.randint(1, 100)
    )

def read_nodes_from_file(filename):
    nodes = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            n = int(f.readline().strip())
            for i in range(n):
                line = f.readline().strip()
                x, y, r, e, p = map(float, line.split())
                nodes.append(Node(i + 1, x, y, r, e, p))  # Start IDs from 1
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return nodes

def write_network_to_file(filename, wsn):
    with open(filename, 'w') as f:
        # Write node information
        f.write(f"{len(wsn.nodes)}\n")
        for node in wsn.nodes:
            f.write(f"{node.x:.2f} {node.y:.2f} {node.r:.2f} {node.e:.2f} {node.p:.2f}\n")

        # Write cluster information
        f.write("\nCluster Information:\n")
        for cluster in wsn.clusters:
            if cluster.nodes:  # Write only clusters with nodes
                f.write(f"Cluster {cluster.cluster_id}:\n")
                f.write(f"  Nodes: {', '.join(str(node.node_id) for node in cluster.nodes)}\n")
                f.write(f"  Clusterhead: {cluster.clusterhead.node_id if cluster.clusterhead else 'None'}\n")

def main():
    while True:
        print("\n1. Random mode")
        print("2. User mode")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Random mode: Initialize WSN with random nodes
            wsn = WSN(20, 20, 5)  # 20x20 grid, 5x5 clusters
            num_nodes = random.randint(10, 100)
            for i in range(num_nodes):
                wsn.add_node(generate_random_node(i))
            wsn.elect_clusterheads()
            write_network_to_file('network.txt', wsn)
            print(f"\nRandom network information has been written to network.txt")

        elif choice == '2':
            # User mode: Initialize WSN with nodes from input.txt
            wsn = WSN(20, 20, 5)
            nodes = read_nodes_from_file('input.txt')
            for node in nodes:
                wsn.add_node(node)
            wsn.elect_clusterheads()
            write_network_to_file('network.txt', wsn)
            print(f"\nNetwork information has been written to network.txt")

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")
            continue

        # Display cluster information
        print("\nCluster Information:")
        for cluster in wsn.clusters:
            if cluster.nodes:
                print(f"Cluster {cluster.cluster_id}:")
                print(f"  Nodes: {', '.join(str(node.node_id) for node in cluster.nodes)}")
                print(f"  Clusterhead: {cluster.clusterhead.node_id if cluster.clusterhead else 'None'}")

        # Handle routing
        while True:
            source = input("\nEnter source node ID (or 'q' to go back to main menu): ")
            if source.lower() == 'q':
                break
            dest = input("Enter destination node ID: ")

            try:
                source_id = int(source)
                dest_id = int(dest)
                route = wsn.route(source_id, dest_id)
                if route:
                    print("Route:", ' -> '.join(str(node.node_id) for node in route))
                else:
                    print("No route found between the specified nodes.")
            except ValueError:
                print("Invalid input. Please enter valid node IDs.")

if __name__ == "__main__":
    main()
