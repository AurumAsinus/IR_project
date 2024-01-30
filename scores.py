import math

# Read query file and organize data
def read_query_file(file_path):
    queries_data = {}

    # Read the file and organize the data
    with open(file_path, 'r') as file:
        current_query_id = None
        for line in file:
            parts = line.split()
            if not parts:
                continue
            else:
                if parts[0] == 'QN':
                    # New query entry
                    current_query_id = parts[1]
                    queries_data[current_query_id] = {'scores': {}}
                elif parts[0] == 'RD':
                    # Add doc_id and score to the current query
                    for i in range(1, len(parts), 2):
                        doc_id = parts[i]
                        score = float(parts[i + 1])
                        queries_data[current_query_id]['scores'][doc_id] = score
                elif line.startswith(' '):
                    numbers = [int(num) for num in line.split()]
                    for i in range(0, len(numbers), 2):
                        queries_data[current_query_id]['scores'][numbers[i]] = numbers[i + 1]

# Keep top 5 for each query
def keep_top_5(queries_data):
    rankings = []
    for query_id, data in queries_data.items():
        scores = data['scores']
        top_5 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
        rankings.append([(doc_id, rank + 1, score) for rank, (doc_id, score) in enumerate(top_5)])
        return rankings

# Print Ranking
for i, query_rankings in enumerate(rankings, start=1):
    print(f"\nQuery {i} Rankings:")
    for doc_id, rank, score in query_rankings:
        print(f"Doc ID: {doc_id}, Rank: {rank}, Score: {score}")

# Extracting relevance values
def extract_relevance_values(queries_data):
    relevance_values = [value for sub_dict in queries_data.values() for value in sub_dict['scores'].values()]
    min_relevance = min(relevance_values)
    max_relevance = max(relevance_values)
    return relevance_values

def custom_round(value):
    decimal_part = value - int(value)
    if decimal_part >= 0.5:
        return math.ceil(value)
    else:
        return round(value)

def min_max_scaling(value, min_val, max_val, min_scale, max_scale):
    scaled_value = (value - min_val) / (max_val - min_val) * (max_scale - min_scale) + min_scale
    return custom_round(scaled_value)

# Scaled relevance values
def scale_relevance_values(relevance_values):
    min_relevance = min(relevance_values)
    max_relevance = max(relevance_values)
    scaled_relevance = [min_max_scaling(value, min_relevance, max_relevance, 0, 4) for value in relevance_values]
    return scaled_relevance

def scaled_dict(queries_data):
    min_relevance = min(relevance_values)
    max_relevance = max(relevance_values)
    scaled_dict = {
        key: {
            'scores': {sub_key: min_max_scaling(sub_value, min_relevance, max_relevance, 0, 4) for sub_key, sub_value in
                    sub_dict['scores'].items()}
        }
        for key, sub_dict in queries_data.items()
    }

def main():
    file_path = "cfquery_detailed"
    queries_data = read_query_file(file_path)
    rankings = keep_top_5(queries_data)

    # Print Rankings
    for i, query_rankings in enumerate(rankings, start=1):
        print(f"\nQuery {i} Rankings:")
        for doc_id, rank, score in query_rankings:
            print(f"Doc ID: {doc_id}, Rank: {rank}, Score: {score}")

    # Extracting relevance values
    relevance_values = extract_relevance_values(queries_data)
    
    # Scaled relevance values
    scaled_relevance = scale_relevance_values(relevance_values)

    # Scaled dictionary
    scaled_dict = scale_dict(queries_data)

if __name__ == "__main__":
    main()

