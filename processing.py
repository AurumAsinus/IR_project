# Read the data from the given format
with open(r"C:\Users\IOANNA\Desktop\IR\cfquery_detailed", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize lists
queries = []
doc_ids = []
relevant_docs = []

# Initialize variables to track the current query and its relevant documents
current_query = None
current_relevant_docs = []

# Iterate through the lines and extract information
for line in lines:
    if line.startswith("QN"):
        # New query
        if current_query is not None:
            # Append the query and its relevant documents
            queries.append(current_query)
            doc_ids.append(current_relevant_docs)
            relevant_docs.append(current_relevant_docs)
        # Reset variables for the new query
        current_query = line.strip().split(maxsplit=1)[1]
        current_relevant_docs = []
    elif line.startswith("RD"):
        # Relevant documents
        doc_scores = line.strip().split()[1:]
        # Append document IDs and scores to the current relevant documents list
        current_relevant_docs.extend([(doc_scores[i], doc_scores[i + 1]) for i in range(0, len(doc_scores), 2)])

# Append the last query and its relevant documents
queries.append(current_query)
doc_ids.append(current_relevant_docs)
relevant_docs.append(current_relevant_docs)

# Write query-doc pairs to a new file
with open(r"C:\Users\IOANNA\Desktop\IR\colbert_dataset.tsv", "w", encoding="utf-8") as output_file:
    for query, doc_scores_list in zip(queries, relevant_docs):
        for doc_id, relevance_score in doc_scores_list:
            output_file.write(f"{query}\t{doc_id}\t{relevance_score}\n")

print("Conversion complete. colbert_dataset.tsv has been created")
