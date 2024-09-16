import random
import math

class Node:
    def __init__(self, id, x, y, r, e, p):
        self.id = id
        self.x = x
        self.y = y
        self.r = r  # Radio range
        self.e = e  # Energy level
        self.p = p  # Processing power
        self.cluster = None  # Initially, the node is not part of any cluster

    def calculate_f(self):
        return 0.4 * self.r + 0.4 * self.e + 0.2 * self.p

    def distance_to(self, other_node):
        return math.sqrt((self.x - other_node.x)**2 + (self.y - other_node.y)**2)

class Cluster:
    def __init__(self, id, x, y, size):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.nodes = []  # List to store nodes belonging to the cluster
        self.clusterhead = None  # Initially, no clusterhead is elected

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)  # Add the node to the cluster's node list
            node.cluster = self  # Set the node's cluster reference to this cluster

    def elect_clusterhead(self):
        if not self.nodes:
            return None  # Return None if there are no nodes in the cluster

        max_f = float('-inf')  # Initialize max F value to negative infinity
        candidates = []  # List to store candidate nodes for clusterhead

        for node in self.nodes:
            f = node.calculate_f()  # Calculate the F value for the node
            if f > max_f:
                max_f = f  # Update the max F value
                candidates = [node]  # Reset candidates list with the new node
            elif f == max_f:
                candidates.append(node)  # Add node to candidates if F value is the same

        if len(candidates) == 1:
            self.clusterhead = candidates[0]  # Single candidate becomes clusterhead
        else:
            # Break tie based on proximity to cluster center
            center_x = self.x + self.size / 2
            center_y = self.y + self.size / 2
            self.clusterhead = min(candidates, key=lambda n: (n.x - center_x)**2 + (n.y - center_y)**2)

        return self.clusterhead  # Return the elected clusterhead

class WSN:
    def __init__(self, width, height, cluster_size):
        self.width = width
        self.height = height
        self.cluster_size = cluster_size
        self.nodes = []  # List to store all nodes in the network
        self.clusters = []  # List to store all clusters in the network
        self._initialize_clusters()  # Initialize clusters across the network area

    def _initialize_clusters(self):
        cluster_id = 0
        for x in range(0, self.width, self.cluster_size):
            for y in range(0, self.height, self.cluster_size):
                self.clusters.append(Cluster(cluster_id, x, y, self.cluster_size))
                cluster_id += 1

    def add_node(self, node):
        self.nodes.append(node)
        cluster_x = int(node.x // self.cluster_size)
        cluster_y = int(node.y // self.cluster_size)
        cluster_index = cluster_y * (self.width // self.cluster_size) + cluster_x
        self.clusters[cluster_index].add_node(node)

    def elect_clusterheads(self):
        for cluster in self.clusters:
            cluster.elect_clusterhead()

    def route(self, source_id, dest_id):
        source = next((node for node in self.nodes if node.id == source_id), None)
        dest = next((node for node in self.nodes if node.id == dest_id), None)

        if not source or not dest:
            print(f"Source or destination node not found. Source ID: {source_id}, Destination ID: {dest_id}")
            return None

        path = [source]
        current = source

        while current != dest:
            neighbors = [node for node in self.nodes if node != current and current.distance_to(node) <= current.r]
            if not neighbors:
                print(f"No neighbors found for node {current.id} within radio range.")
                return None  # No route found

            next_hop = min(neighbors, key=lambda n: n.distance_to(dest))
            if next_hop in path:
                print(f"Loop detected. Node {next_hop.id} is already in the path.")
                return None  # Prevent loops
            path.append(next_hop)
            current = next_hop

        return path

def generate_random_node(id):
    return Node(
        id,
        random.uniform(0, 20),
        random.uniform(0, 20),
        random.uniform(1, 8),
        random.uniform(1, 100),
        random.uniform(1, 100)
    )

def read_nodes_from_file(filename):
    nodes = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            n = int(f.readline().strip())
            for i in range(n):
                line = f.readline().strip()
                try:
                    x, y, r, e, p = map(float, line.split())
                    nodes.append(Node(i, x, y, r, e, p))
                except ValueError as ve:
                    print(f"Error parsing line {i + 2}: {line}")
                    print(f"ValueError: {ve}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return nodes

def write_network_to_file(filename, wsn):
    with open(filename, 'w') as f:
        f.write(f"{len(wsn.nodes)}\n")
        for node in wsn.nodes:
            f.write(f"{node.x:.2f} {node.y:.2f} {node.r:.2f} {node.e:.2f} {node.p:.2f}\n")

        f.write("\nCluster Information:\n")
        for cluster in wsn.clusters:
            f.write(f"Cluster {cluster.id}:\n")
            f.write(f"  Nodes: {', '.join(str(node.id) for node in cluster.nodes)}\n")
            f.write(f"  Clusterhead: {cluster.clusterhead.id if cluster.clusterhead else 'None'}\n")

def main():

    while True:
        print("\n1. Random mode")
        print("2. User mode")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Reinitialize WSN for Random mode
            wsn = WSN(20, 20, 5)  # Initialize a 20x20 network with 5x5 clusters
            num_nodes = random.randint(10, 100)
            for i in range(num_nodes):
                wsn.add_node(generate_random_node(i))
            wsn.elect_clusterheads()
            write_network_to_file('network_random.txt', wsn)  # Save random mode data to network_random.txt
            print(f"\nRandom network information has been written to network_random.txt")
        elif choice == '2':
            # Reinitialize WSN for User mode
            wsn = WSN(20, 20, 5)  # Initialize a 20x20 network with 5x5 clusters
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

        print("\nCluster Information:")
        for cluster in wsn.clusters:
            print(f"Cluster {cluster.id}:")
            print(f"  Nodes: {', '.join(str(node.id) for node in cluster.nodes)}")
            print(f"  Clusterhead: {cluster.clusterhead.id if cluster.clusterhead else 'None'}")

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
                    print("Route:", ' -> '.join(str(node.id) for node in route))
                else:
                    print("No route found between the specified nodes.")
            except ValueError:
                print("Invalid input. Please enter valid node IDs.")

if __name__ == "__main__":
    main()