# TO DOs
# 1. Handling Term Variations


import numpy as  np
import math
from nltk.corpus import stopwords
import nltk
import pandas as pd
import os
nltk.download('stopwords')

# Define stop words
stop_words = set(stopwords.words('english'))

# Load queries from TSV file
query_file_path = r"C:\Users\IOANNA\Desktop\IR\queries.tsv"
queries = pd.read_csv(query_file_path, sep='\t')
queries = list(queries['Query'])
#print(queries)

# Load documents (OK)
def load_docs(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        doc_id = filename
        with open(os.path.join(folder_path, filename), 'r') as file :
            content = file.read().replace('\n', ' ').strip()
            documents[doc_id] = content
    return documents

docs_folder_path = r"C:\Users\IOANNA\Desktop\IR\docs"
documents = load_docs(docs_folder_path)
#print(documents['01239'])


# Calculate TFij vectors - Frequency of words in each doc
def tfij(docs):
    tfij_vectors = []
    for doc in docs.values():
        # Tokenize document and remove stop words
        terms = [term for term in doc.lower().split() if term not in stop_words]
        #print(terms)
        # Calculate TFij for each term in the doc
        tfij_vector = {}
        for term in terms :
            if term not in tfij_vector:
                tfij_vector[term] = 1
            else :
                tfij_vector[term] += 1
        tfij_vectors.append(tfij_vector)
    return tfij_vectors

# Calculate IDFi vectors
def idfi(tfij_vectors):
    idfi_vector = {}
    total_docs = len(tfij_vectors)

    # Calculate document frequency for each term
    for tfij_vector in tfij_vectors:
        # Calculate the # of docs containing each term
        for term in tfij_vector:
            if term not in idfi_vector:
                idfi_vector[term] = 1
            else :
                idfi_vector[term] += 1

    # Calculate IDF for each term
    for term in idfi_vector:
        idfi_vector[term] = math.log(total_docs/idfi_vector[term])
    return idfi_vector

# Calculate TF-IDF vectors
def tfidf(tfij_vectors, idfi_vector):
    tfidf_vectors = []

    for tfij_vector in tfij_vectors:
        # Calculate TF-IDF for each term in the document  
        tfidf_vector = {}
        for term, tfij_value in tfij_vector.items():
            tfidf_vector[term] = tfij_value * idfi_vector.get(term, 0)
        tfidf_vectors.append(tfidf_vector)

    return tfidf_vectors 

# Construct document vectors
def const_doc_vectors(tfidf_vectors):
    doc_vectors = []
    max_vector_length = max(len(tfidf_vector) for tfidf_vector in tfidf_vectors)

    for tfidf_vector in tfidf_vectors:
        doc_vector = np.zeros(max_vector_length)
        for idx, (term, value) in enumerate(tfidf_vector.items()):
            doc_vector[idx] = value
        doc_vectors.append(normalize_vector(doc_vector))  # Normalize each document vector

    return doc_vectors


# Construct query vectors
def const_query_vectors(query, idfi_vector, max_vector_length):
    # Tokenize query and remove stop words
    terms = [term for term in query.lower().split() if term not in stop_words]

    # Calculate TFij for each term in the query
    tfij_vector = {}
    for term in terms:
        if term not in tfij_vector:
            tfij_vector[term] = 1
        else:
            tfij_vector[term] += 1

    # Calculate TF-IDF for each term in the query
    query_vector = np.zeros(max_vector_length)
    for idx, (term, value) in enumerate(idfi_vector.items()):
        if idx < max_vector_length:
            query_vector[idx] = tfij_vector.get(term, 0) * value

    # Normalize the query vector
    query_vector = normalize_vector(query_vector)

    return query_vector

# To be used for normalization
def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector/norm


# Calculate cosine similarity
def cosine_similarity(doc_vector, query_vector):
    dot_product = np.dot(doc_vector, query_vector)
    norm_doc = np.linalg.norm(doc_vector)
    norm_query = np.linalg.norm(query_vector)

    if np.isclose(norm_doc, 0.0) or np.isclose(norm_query, 0.0) or np.isnan(norm_doc) or np.isnan(norm_query):
        return 0.0  # Return 0 if either vector has zero norm or is NaN

    similarity = dot_product / (norm_doc * norm_query)

    # Print debug information
    # print("Dot Product:", dot_product)
    # print("Norm Doc:", norm_doc)
    # print("Norm Query:", norm_query)
    # print("Similarity:", similarity)

    return similarity


def main():
    # Step 1
    tfij_vectors = tfij(documents)
    #tfij_vectors = tfij(dict(list(documents.items())[:10]))
    #print("TFij Vectors :")
    #print(tfij_vectors)

    # Step 2
    idfi_vector = idfi(tfij_vectors)
    #print("\nIDFi Vector:")
    #print(idfi_vector)

    # Step 3
    tfidf_vectors = tfidf(tfij_vectors, idfi_vector)
    #print("\nTF-IDF Vectors:")
    #print(tfidf_vectors)

    # Document Vectors
    doc_vectors =  const_doc_vectors(tfidf_vectors)
    #print("\nDocument Vectors:")
    #print(doc_vectors)

    query_vectors = []

    #for doc_id, doc_vector in zip(documents.keys(), doc_vectors):
        #print(f"\n Document {doc_id} Vector : {doc_vector}")

    # print("TFij Vectors:")
    # print(tfij_vectors)

    # print("\nIDFi Vector:")
    # print(idfi_vector)

    # print("\nTF-IDF Vectors:")
    # print(tfidf_vectors)


    # Query Vectors
    max_vector_length = max(len(tfidf_vector) for tfidf_vector in tfidf_vectors)
    
    rankings = [[] for _ in range(len(queries))]

    for i, query in enumerate(queries, start=1):
        query_vector = const_query_vectors(query, idfi_vector, max_vector_length)
        #print(f"\nQuery Vector {i}: {query_vector}")
        similarities = []
        # Similarity
        for doc_id, doc_vector in zip(documents.keys(), doc_vectors):
            similarity = cosine_similarity(doc_vector, query_vector)
            if np.isnan(similarity) or similarity == 0.0:
                continue
            elif (similarity > 0.01):
                similarities.append((doc_id, similarity))
                #print(f"\nSimilarity with Doc {doc_id} for Query {i}: {similarity}")
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_5 = similarities[:5]

        for rank, (doc_id, score) in enumerate(top_5, start=1):
            rankings[i-1].append((doc_id, rank, score))

    for i, query_rankings in enumerate(rankings, start=1):
        print(f"\nQuery {i} Rankings:")
        for doc_id, rank, score in query_rankings:
            print(f"Doc ID: {doc_id}, Rank: {rank}, Score: {score}")
    
if __name__ == "__main__":
    main()


