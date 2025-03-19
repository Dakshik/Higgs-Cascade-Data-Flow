import json
import csv
from collections import defaultdict

# File paths
input_file = "higgs-activity_time.txt"  
json_output_file = "higgs_mentions.json"
csv_output_file = "higgs_mentions.csv"

# Initialize data structure
mention_cascades = defaultdict(lambda: defaultdict(list))

# Process the input file
with open(input_file, "r") as file:
    for line in file:
        # Parse each line into userA, userB, timestamp, and interaction
        parts = line.strip().split()
        if len(parts) == 4:
            userA, userB, timestamp, interaction = parts
            try:
                userA, userB, timestamp = int(userA), int(userB), int(timestamp)
                if interaction == "MT":  # Filter for mentions only
                    mention_cascades[userA][timestamp].append(userB)
            except ValueError:
                print(f"Skipping malformed line: {line.strip()}")

# Prepare JSON structure: Group by userA and sort timestamps
formatted_mentions = {
    str(userA): [
        {"timestamp": timestamp, "mentions": mentions}
        for timestamp, mentions in sorted(timestamps.items())
    ]
    for userA, timestamps in mention_cascades.items()
}

# Write JSON output
with open(json_output_file, "w") as json_file:
    json.dump(formatted_mentions, json_file, indent=4)

print(f"Mentions data saved to {json_output_file}")

# Write CSV output
with open(csv_output_file, "w", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Initiator", "Timestamp", "Mentions"])
    for userA, interactions in formatted_mentions.items():
        for interaction in interactions:
            timestamp = interaction["timestamp"]
            mentions = ", ".join(map(str, interaction["mentions"]))
            writer.writerow([userA, timestamp, mentions])

print(f"Mentions data saved to {csv_output_file}")
