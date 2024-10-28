import json
import csv
import argparse

def generate_gephi_files(json_path, target_account, nodes_output, edges_output):
    # Load the JSON data
    with open(json_path, 'r') as f:
        followers = json.load(f)

    # Write the Nodes CSV file
    with open(nodes_output, 'w', newline='') as node_file:
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

            # if follower_count >= 10000:
            node_writer.writerow([user_id, user_id, follower_count, node_color])

    # Write the Edges CSV file
    with open(edges_output, 'w', newline='') as edge_file:
        edge_writer = csv.writer(edge_file)
        edge_writer.writerow(['Source', 'Target', 'Type'])  # Gephi edge columns

        # Add an edge from central account to each follower
        for follower in followers:
            follower_count = follower['stats']['followerCount']
            # if follower_count >= 10000:
            user_id = follower['user']['uniqueId']
            edge_writer.writerow([target_account, user_id, 'Undirected'])

def main():
    parser = argparse.ArgumentParser(description="Generate Gephi nodes and edges CSV files from JSON data")
    parser.add_argument("-j", "--json_path", required=True, help="Path to the source JSON file with follower data")
    parser.add_argument("-t", "--target_account", required=True, help="The central account node")
    parser.add_argument("-n", "--nodes_output", required=True, help="Output filename for nodes CSV file")
    parser.add_argument("-e", "--edges_output", required=True, help="Output filename for edges CSV file")
    args = parser.parse_args()

    generate_gephi_files(args.json_path, args.target_account, args.nodes_output, args.edges_output)

if __name__ == "__main__":
    main()
