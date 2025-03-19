# Higgs Dataset - JSON Format Explanation

## Description
This document explains the structure of the Higgs dataset, which contains Twitter mention interactions related to the discovery of the Higgs boson. The dataset captures how users mention each other over time, forming a network of interactions. The JSON format provides a structured representation of this mention flow, making it easier for data analysis and visualization.

## JSON Data Format
The dataset is stored as a list of JSON objects, where each object represents a single user's mentions over time.

## JSON Structure
Each JSON object consists of two key fields:

```json
{
    "user_id": 223789,
    "mentions": [
        { "timestamp": 1341100972, "mentioned_users": [213163] },
        { "timestamp": 1341413739, "mentioned_users": [66977] },
        { "timestamp": 1341445126, "mentioned_users": [2994] }
    ]
}
```

## Field Breakdown
- **`user_id`**: The ID of the user making mentions.
- **`mentions`**: A list of mention events by the user.
  - **`timestamp`**: The Unix timestamp when the mention was made.
  - **`mentioned_users`**: A list of user IDs mentioned in the event.

## Understanding the Mention Flow
Each user in the dataset initiates a set of mentions over time, forming a directed network of interactions.

### Example Mentions List Breakdown:

```json
"mentions": [
    { "timestamp": 1341100972, "mentioned_users": [213163] },
    { "timestamp": 1341413739, "mentioned_users": [66977] },
    { "timestamp": 1341445126, "mentioned_users": [2994] }
]
```

- **User `223789`** → Mentions **User `213163`** at **timestamp 1341100972**.
- **User `223789`** → Mentions **User `66977`** at **timestamp 1341413739**.
- **User `223789`** → Mentions **User `2994`** at **timestamp 1341445126**.

This hierarchical format allows for **tracking how information propagates** within Twitter conversations over time.

## Explaining the Mention Path
Each participant in the dataset follows a structured mention path:
- **Direct Mentions**: If a user directly mentions another user, it appears as a single mention event.
- **Multiple Mentions**: If a user mentions multiple users in a single event, all mentioned users appear under `mentioned_users`.

### Example Breakdown:

```json
{"timestamp": 1341100972, "mentioned_users": [213163, 66977]}
```

- **User `223789`** mentioned both **Users `213163` and `66977`** at the same timestamp.
- This means both users were part of the conversation initiated by `223789` at that specific moment.

## Example Code
Below is a snippet of `visualize-mentions.py`, which loads the dataset and generates a visualization of mention interactions:

```python
import pandas as pd
import matplotlib.pyplot as plt

def plot_mentions(json_file):
    with open(json_file, 'r') as f:
        data = pd.read_json(f)
    mentions_count = []
    timestamps = []
    
    for user in data:
        for mention in user['mentions']:
            timestamps.append(mention['timestamp'])
            mentions_count.append(len(mention['mentioned_users']))
    
    df = pd.DataFrame({'timestamp': timestamps, 'mention_count': mentions_count})
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.groupby(df['timestamp'].dt.date)['mention_count'].sum().plot(kind='line')
    plt.xlabel("Date")
    plt.ylabel("Number of Mentions")
    plt.title("Mentions Over Time")
    plt.show()

plot_mentions("higgs_mentions.json")
```

### How to Read This Code
- **Reads JSON file**: Loads `higgs_mentions.json` and extracts mention data.
- **Extracts timestamps and mention counts**: Iterates through the dataset to record mention occurrences.
- **Converts timestamps**: Converts Unix timestamps to readable dates.
- **Aggregates mentions per day**: Groups data by date and calculates the total mentions per day.
- **Plots the mentions over time**: Generates a line chart showing the trend of mentions.

## Applications
This dataset can be used for:
- **Social Network Analysis**: Understanding user interactions and information spread.
- **Trend Analysis**: Identifying key influencers and discussion patterns.
- **Graph Modeling**: Mapping relationships and propagations within conversations.


