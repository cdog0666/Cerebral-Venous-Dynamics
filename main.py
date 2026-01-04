
# For Each Of The Imports You Have To Go To Terminal And Instal The Package Using pip install <package-name>
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd 
from pyvis.network import Network

# Read CSV file
df = pd.read_csv("Atlas_Anatomy-EdgeNode_01-01 - Sheet1.csv")

# Create a directed graph
G = nx.DiGraph()

# Populate directed graph with csv data
for row in df.itertuples():
    G.add_edge(row.A,row.B)

net = Network(height="600px", width="100%", directed=True)
net.from_nx(G)
net.write_html("graph.html")

# Draw
pos = nx.spring_layout(G, k=0.5, iterations=50) #layout for better visualization
nx.draw(G, pos, with_labels=True, arrows=True, node_size=200)
plt.show()