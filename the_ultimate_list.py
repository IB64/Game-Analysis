import json
import os

def merge_json_files(input_dir, output_file):
    merged_data = {}
    
    # Loop through each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                # Merge data from each file
                for game_id, item in data.items():
                    if game_id not in merged_data:
                        merged_data[game_id] = item
                    else:
                        # Handle duplicate game IDs if needed
                        # For now, let's skip duplicates
                        pass
    
    # Write the merged data to the output file
    with open(output_file, 'w') as out_file:
        json.dump(merged_data, out_file, indent=4)

def remove_dupes(steam_ids: list) -> None:
    banana = list(set(steam_ids))
    return banana

if __name__ == "__main__":
    # with open("steam_ids.txt", "r") as file:
    #     content = file.read().splitlines()
    # new_ultimate_list = remove_dupes(content)

    # with open("ultimate_steam_ids.txt", "w") as file:
    #     for id in new_ultimate_list:
    #         file.write(id + "\n")

    # Example usage
    input_directory = './genres'  # directory containing JSON files to be merged
    output_file = 'merged.json'      # output file to store merged JSON data

    merge_json_files(input_directory, output_file)
        
        