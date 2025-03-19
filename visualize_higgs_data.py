import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the JSON data
json_file_path = "higgs_mentions.json"  
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

# Prompt the user to enter a specific user ID
userA_to_visualize = input("Enter the user ID to visualize their mentions: ").strip()

# Check if the user exists in the data
if userA_to_visualize not in data:
    print(f"User {userA_to_visualize} not found in the dataset.")
else:
    interactions = data[userA_to_visualize]

    # Initialize a directed graph for the single interaction
    G = nx.DiGraph()

    # Add nodes and edges for the selected userA
    for interaction in interactions:
        timestamp = interaction["timestamp"]
        mentions = interaction["mentions"]

        for userB in mentions:
            G.add_node(userA_to_visualize)  # Add the initiator node
            G.add_node(userB)  # Add mentioned users as nodes
            G.add_edge(userA_to_visualize, userB, timestamp=timestamp)  # Add directed edge

    # Draw the graph
    plt.figure(figsize=(12, 8))
    pos = nx.shell_layout(G)  # Use shell layout for a clean circular arrangement

    # Draw nodes with user IDs
    nx.draw_networkx_nodes(G, pos, node_size=1600, node_color="lightblue", edgecolors="black")
    nx.draw_networkx_labels(G, pos, labels={node: str(node) for node in G.nodes()}, font_size=10)

    # Draw directed edges with timestamps as labels
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="grey")
    edge_labels = nx.get_edge_attributes(G, "timestamp")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Customize plot
    plt.title(f"Interaction Cascade for User {userA_to_visualize}")
    plt.axis("off")  # Turn off axis for cleaner visualization

    # Show the plot
    plt.show()
