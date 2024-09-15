# Wireless Sensor Network (WSN) Simulation

This project simulates a Wireless Sensor Network (WSN) where nodes are distributed in a 2D space and grouped into clusters. Each cluster elects a clusterhead based on certain criteria, and nodes can communicate with each other within their radio range.

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

1. Initializing the network with a specified width, height, and cluster size.
2. Adding nodes to the network either randomly or from a user-provided input file.
3. Assigning nodes to clusters based on their coordinates.
4. Electing a clusterhead for each cluster based on the highest F value.
5. Finding a route between two nodes if they are within each other's radio range.

## File Descriptions

## File Descriptions

- `main.py`: The main script to run the WSN simulation.
- `input.txt`: The input file containing node information.
- `network.txt`: The output file containing the network and cluster information after running the simulation.

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
   Ensure input.txt is formatted correctly (see below).
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
3.00 1.00 4.00 40.00 30.00
2.00 7.00 5.00 99.00 55.00
13.00 14.00 4.00 45.00 80.00
```

## Output File Format

```
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
