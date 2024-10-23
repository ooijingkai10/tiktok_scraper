import json
import csv

# Load your JSON data
with open('combined.json', 'r') as f:
    followers = json.load(f)

# Define the central node
target_account = 'lazada_sg'

# Write the Nodes CSV file
with open('nodes.csv', 'w', newline='') as node_file:
    node_writer = csv.writer(node_file)
    node_writer.writerow(['Id', 'Label', 'FollowerCount', 'Color'])  # Gephi node columns

    # Add central account node
    node_writer.writerow([target_account, target_account, '', 'green'])

    # Add each follower as a node
    for follower in followers:
        user_id = follower['user']['uniqueId']
        follower_count = follower['stats']['followerCount']
        
        # Determine color based on follower count
        if follower_count >= 100000:
            node_color = 'red'
        elif follower_count >= 50000:
            node_color = 'yellow'
        else:
            node_color = 'blue'
        if follower_count >= 10000:
            node_writer.writerow([user_id, user_id, follower_count, node_color])

# Write the Edges CSV file
with open('edges.csv', 'w', newline='') as edge_file:
    edge_writer = csv.writer(edge_file)
    edge_writer.writerow(['Source', 'Target', 'Type'])  # Gephi edge columns

    # Add an edge from central account to each follower
    for follower in followers:
        follower_count = follower['stats']['followerCount']
        if follower_count >= 10000:
            user_id = follower['user']['uniqueId']
            edge_writer.writerow([target_account, user_id, 'Undirected'])
