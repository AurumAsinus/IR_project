import os

# Read the TSV file and store relevant information
query_passages = {}
with open(r"C:\Users\IOANNA\Desktop\IR\colbert_dataset.tsv", "r", encoding="utf-8") as tsv_file:
    for line in tsv_file:
        parts = line.strip().split('\t')
        query, doc_id, relevance_score = parts[0], parts[1], parts[2]

        # Store relevant information in a dictionary
        if query not in query_passages:
            query_passages[query] = []
        query_passages[query].append((doc_id, relevance_score))

# Folder with all 1204 passages
passages_folder = r"C:\Users\IOANNA\Desktop\IR\docs"

# Output TSV file for organized passages
output_tsv_path = r"C:\Users\IOANNA\Desktop\IR\output_colbert_dataset.tsv"
with open(output_tsv_path, "w", encoding="utf-8") as output_file:
    for query, doc_ids_and_scores in query_passages.items():
        for doc_id, relevance_score in doc_ids_and_scores:
            # Construct the filename based on your file naming convention
            filename = f"{int(doc_id):05d}"  # Assuming doc_id already has the format "00001", "00002", ...
            passage_file_path = os.path.join(passages_folder, filename)

            # Check if the passage file exists
            if os.path.exists(passage_file_path):
                # Read the passage content directly from the file
                with open(passage_file_path, "r", encoding="utf-8") as passage_file:
                    passage_content = passage_file.read()

                # Write the passage details to the output TSV file
                output_line = f"{query}\t{doc_id}\t{relevance_score}\t{passage_content}\n"
                output_file.write(output_line)
            else:
                print(f"File not found: {passage_file_path}")

print("Passages organized and saved to TSV.")
