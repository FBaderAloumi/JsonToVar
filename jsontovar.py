import json
import sys
import csv

def convert_appsettings_to_pipeline_variables(json_file_path, csv_file_path):
    try:
        with open(json_file_path, 'r') as file:
            appsettings = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
        print(f"JSONDecodeError: {e.msg}")
        print(f"Error occurred at line {e.lineno}, column {e.colno} (char {e.pos})")
        # Print the line where the error occurred for better debugging
        with open(json_file_path, 'r') as file:
            lines = file.readlines()
            error_line = lines[e.lineno - 1].strip()
            print(f"Error line: {error_line}")
        return

    variables = []

    def collect_variables(prefix, data):
        if isinstance(data, dict):
            for key, value in data.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                collect_variables(new_prefix, value)
        else:
            variables.append((prefix, data))
    
    collect_variables('', appsettings)

    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['JSON Path', 'Value'])
            writer.writerows(variables)
        print(f"Variables successfully written to {csv_file_path}")
    except IOError:
        print(f"Error: Unable to write to file '{csv_file_path}'")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python jsontovar.py <path_to_appsettings.json> <output_csv_file>")
    else:
        json_file_path = sys.argv[1]
        csv_file_path = sys.argv[2]
        convert_appsettings_to_pipeline_variables(json_file_path, csv_file_path)
