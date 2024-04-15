import re

def process_gcode(file_path):
    # Dictionary to store G-code commands and their counts
    gcode_counts = {}

    # Regular expression pattern to match G-codes
    g_pattern = re.compile(r'G\d+')

    # Read the file
    with open(file_path, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Find all G-code commands in the line
            g_matches = g_pattern.findall(line)
            # Update counts for each G-code command found
            for g_code in g_matches:
                if g_code in gcode_counts:
                    gcode_counts[g_code] += 1
                else:
                    gcode_counts[g_code] = 1

    return gcode_counts

def main():
    file_path = '20mm_cube.gcode'  # Replace with the path to your file
    gcode_counts = process_gcode(file_path)

    # Print the results
    print("G-code commands and their counts:")
    for g_code, count in gcode_counts.items():
        print(f"{g_code}: {count}")

if __name__ == "__main__":
    main()
