import os
import json

def combine_json_files(input_folder, output_file):
    combined_data = []

    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):  # Ensure the data is a list
                    combined_data.extend(data)  # Combine lists into one

    # Write the combined data to the output file
    with open(output_file, 'w') as f:
        json.dump(combined_data, f, indent=4)

# Set input folder and output file paths
input_folder = './scraped'
output_file = './scraped/combined.json'

# Combine the files
combine_json_files(input_folder, output_file)
