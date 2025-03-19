import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the JSON data containing mentions
json_file_path = "higgs_mentions.json"  
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

# Initialize a directed graph
G = nx.DiGraph()

# Add a root node for the hierarchical graph (e.g., 'root_user')
root_user = "root_user"  # Set a root for the tree
G.add_node(root_user)

# Add nodes and edges for the first 100 mentions
mention_count = 0
max_mentions = 100  # Limit to the first 100 mentions

for userA, interactions in data.items():
    G.add_edge(root_user, userA)  # Connect all starting nodes to the root
    
    for interaction in interactions:
        timestamp = interaction["timestamp"]
        mentions = interaction["mentions"]

        for userB in mentions:
            if mention_count < max_mentions:
                G.add_node(userA)  # Add starting user node
                G.add_node(userB)  # Add mentioned user node
                G.add_edge(userA, userB, timestamp=timestamp)  # Add directed edge with timestamp
                mention_count += 1
            else:
                break
        if mention_count >= max_mentions:
            break
    if mention_count >= max_mentions:
        break

# Draw the hierarchical graph
plt.figure(figsize=(18, 12))

# Use Graphviz dot layout for a tree structure
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')  # Forces hierarchical layout

# Draw nodes with user IDs
nx.draw_networkx_nodes(G, pos, node_size=1600, node_color="lightblue", edgecolors="black")
nx.draw_networkx_labels(G, pos, labels={node: str(node) for node in G.nodes()}, font_size=8)

# Draw directed edges with timestamps as labels
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, edge_color="grey")
edge_labels = nx.get_edge_attributes(G, "timestamp")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

# Customize plot
plt.title("Hierarchical Mentions Network (First 100 Mentions)")
plt.axis("off")  # Turn off axis for cleaner visualization

# Show the plot
plt.show()
