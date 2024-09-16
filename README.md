## github link:https://github.com/Dharmareddy8520/wsn1

# Wireless Sensor Network (WSN) Simulation

This project simulates the operation of a clustered Wireless Sensor Network (WSN) within a 20m x 20m square area. The network is divided into 16 uniform clusters, and the nodes are randomly or manually assigned to these clusters based on their coordinates. Each cluster elects a clusterhead based on certain criteria, and nodes can communicate with each other within their radio range.

## Table of Contents

- [Introduction](#introduction)
- [File Descriptions](#file-descriptions)
- [How to Run](#how-to-run)
- [Input File Format](#input-file-format)
- [Output File Format](#output-file-format)
- [Classes and Methods](#classes-and-methods)
- [Example](#example)

## Introduction

The WSN simulation involves the following steps:

1. Cluster Assignment: Each node is assigned to a predetermined cluster based on its coordinates.
2. The program operates in two modes:

   1. Random Mode: The program generates a random number of nodes (between 10 and 100), assigns random characteristics (position, radio range, energy, and processing power), and simulates the network.
   2. User Mode: The program reads node characteristics from a file (input.txt) and simulates the network based on user-provided node details.

3. Clusterhead Election: The node with the highest calculated score (based on radio range, energy, and processing power) is elected as the clusterhead for each cluster. In case of a tie, the node closest to the cluster center is chosen.

4. Greedy Routing: Nodes route packets to the nearest neighbor within radio range that is closest to the destination node.

5. Output to File: The network structure, including node details and cluster information, is written to an output file (network.txt or network_random.txt).

6. Routing Display: The program displays the routing path (series of hops) from the source node to the destination node.

## File Descriptions

## File Descriptions

- `main.py`: The main script to run the WSN simulation.
- `input.txt`: The input file containing node information.
- `network.txt`: The output file containing the network and cluster information after running the simulation taking input from input.txt file
- `network_random` :The output file containing the network and cluster information after running the simulation taking input from random generator

## How to Run

1. **Run the Program**:
   ```sh
   python main.py
   ```
2. **Choose Mode**:
   ```
   Enter 1 for Random mode.
   Enter 2 for User mode.
   Enter 3 to Quit.
   User Mode:
   ```
3. **User Mode**
   ```
   Ensure input.txt is formatted correctly .
   The program will read nodes from input.txt and write the network information to network_user.txt.
   ```
4. **Random Mode**
   ```
   The program will generate a random number of nodes and write the network information to network_random.txt.
   ```
5. **Routing**
   ```
    Enter source and destination node IDs to find a route between them
   ```

## Input File Format

    ```
    The input.txt file should contain the following information:
    The number of nodes.
    Each node's details in the format: x y r e p, where:
    x: x-coordinate
    y: y-coordinate
    r: radio range
    e: energy level
    p: processing pow
    ```

## Example

```
3
3 1 4 40 30
2 7 5 99 55
13 14 4 45 80

```

## Output File Format

```
In Random Mode, the program outputs network details to network_random.txt.
In User Mode, the program outputs network details to network.txt.

The network.txt file will contain:

The number of nodes.
Each node's details.
Cluster information including nodes and clusterhead.
3
3.00 1.00 4.00 40.00 30.00
2.00 7.00 5.00 99.00 55.00
13.00 14.00 4.00 45.00 80.00

Cluster Information:
Cluster 0:
  Nodes: 0
  Clusterhead: 0
Cluster 1:
  Nodes:
  Clusterhead: None
Cluster 2:
  Nodes:
  Clusterhead: None
Cluster 3:
  Nodes:
  Clusterhead: None
Cluster 4:
  Nodes: 1
  Clusterhead: 1
Cluster 5:
  Nodes:
  Clusterhead: None
Cluster 6:
  Nodes:
  Clusterhead: None
Cluster 7:
  Nodes:
  Clusterhead: None
Cluster 8:
  Nodes:
  Clusterhead: None
Cluster 9:
  Nodes:
  Clusterhead: None
Cluster 10:
  Nodes: 2
  Clusterhead: 2
Cluster 11:
  Nodes:
  Clusterhead: None
Cluster 12:
  Nodes:
  Clusterhead: None
Cluster 13:
  Nodes:
  Clusterhead: None
Cluster 14:
  Nodes:
  Clusterhead: None
Cluster 15:
  Nodes:
  Clusterhead: None
```
