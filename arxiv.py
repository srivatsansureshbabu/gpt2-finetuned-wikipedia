import pinecone
import numpy as np
from pinecone import Pinecone, ServerlessSpec
import os
def intializeEmbeddings():
    pc = Pinecone(api_key=os.getenv("PINECONE_API"), environment="us-east-1")  # match the dashboard region

    index_name = "arxiv-index"
    index = pc.Index(index_name)  # index must already exist in this region
    return index

def searchPapers(model, index, cursor, query_text, top_k=5):
    # 1. Generate embedding
    query_embedding = model.encode([query_text])[0]

    # 2. Normalize for cosine similarity (optional)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    # 3. Convert to plain Python floats
    query_embedding = [float(x) for x in query_embedding]

    # 4. Query Pinecone
    result = index.query(vector=[query_embedding], top_k=top_k)

    papers = []
    for match in result['matches']:
        # Extract numeric part of Pinecone ID
        row_offset = int(match['id'].replace("paper", ""))

        # Fetch paper metadata from SQLite
        cursor.execute("SELECT title, abstract FROM papers LIMIT 1 OFFSET ?", (row_offset,))
        row = cursor.fetchone()
        if row:
            title, abstract = row
        else:
            title, abstract = "Unknown", ""

        papers.append({
            "id": match['id'],
            "score": match['score'],
            "title": title,
            "abstract": abstract
        })

    return papers


def doiToArxiv(doi):
    """
    Converts an arXiv DOI into the corresponding arXiv URL.
    
    Example:
        doi = "10.48550/arXiv.2308.12345"
        returns "https://arxiv.org/abs/2308.12345"
    """
    try:
        # Extract the arXiv ID from the DOI
        arxiv_id = doi.split(".")[-1]
        return f"https://arxiv.org/abs/{arxiv_id}"
    except Exception as e:
        print(f"Error converting DOI: {e}")
        return None
