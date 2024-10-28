import os
import json
import argparse

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

def main():
    parser = argparse.ArgumentParser(description="Combine multiple JSON files in a folder into a single JSON file.")
    parser.add_argument("-i", "--input_folder", required=True, help="Path to the input folder containing JSON files")
    parser.add_argument("-o", "--output_file", required=True, help="Output filename for the combined JSON file")
    args = parser.parse_args()

    combine_json_files(args.input_folder, args.output_file)

if __name__ == "__main__":
    main()
