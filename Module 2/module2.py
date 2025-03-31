import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random

# Generate users and content items
users = [f"User_{i}" for i in range(1, 11)]  # 10 users
content = [f"Content_{j}" for j in range(1, 8)]  # 7 content items

# Simulate user-content interactions
interactions = [(random.choice(users), random.choice(content)) for _ in range(25)]
df = pd.DataFrame(interactions, columns=["User", "Content"])

# Create a bipartite graph (Users ↔ Content)
G = nx.Graph()
G.add_nodes_from(users, bipartite=0)  # Users as one set
G.add_nodes_from(content, bipartite=1)  # Content as another set
G.add_edges_from(interactions)  # Add interactions as edges

# Compute centrality metrics
degree_centrality = nx.degree_centrality(G)  
page_rank = nx.pagerank(G)  
betweenness_centrality = nx.betweenness_centrality(G)  

# Store centrality scores for content nodes
content_scores = {
    node: {
        "Degree": degree_centrality[node],
        "PageRank": page_rank[node],
        "Betweenness": betweenness_centrality[node]
    }
    for node in content
}

# Convert to DataFrame for easier analysis
content_df = pd.DataFrame.from_dict(content_scores, orient="index")
print("\nContent Centrality Scores:\n", content_df.sort_values(by="PageRank", ascending=False))

# Visualizing the user-content interaction network
plt.figure(figsize=(10, 6))

# Use a force-directed layout for better visualization
pos = nx.spring_layout(G, seed=42)

# Draw nodes (users and content in different colors)
nx.draw_networkx_nodes(G, pos, nodelist=users, node_color="lightblue", node_size=500, label="Users")
nx.draw_networkx_nodes(G, pos, nodelist=content, node_color="lightcoral", node_size=800, label="Content")

# Draw edges representing interactions
nx.draw_networkx_edges(G, pos, alpha=0.5)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title("User-Content Interaction Network")
plt.legend()
plt.show()

