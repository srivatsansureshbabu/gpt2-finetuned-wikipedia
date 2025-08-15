from arxiv import *
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from arxiv import *
import gradio as gr
from dotenv import load_dotenv

def main():

    # Initialize embeddings and model
    load_dotenv()
    index = intializeEmbeddings()
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    conn = sqlite3.connect(
        "/Users/srivatsansureshbabu/Desktop/FineTuningGPT/arxiv_papers.db",
        check_same_thread=False
    )  
    cursor = conn.cursor()

    def query_papers(query_text, top_k=5):
        results = searchPapers(model, index, cursor, query_text, top_k=top_k)
        output = ""
        for i, paper in enumerate(results, 1):
            doi_link = f"https://doi.org/{paper['doi']}" if 'doi' in paper else "No DOI"
            output += f"{i}. {paper['title']} (score: {paper['score']:.3f})\n"
            output += f"Abstract: {paper['abstract'][:300]}...\n"
            output += f"Link: {doi_link}\n\n"
        return output

    iface = gr.Interface(
        fn=query_papers, 
        inputs=[gr.Textbox(label="Enter your query"), gr.Slider(1, 10, step=1, label="Amount of research papers to return")],
        outputs="textbox",
        title="Arxiv Paper Search Chatbot",
        description="Search over 450K ML & AI research papers and find the most relevant results instantly."
    )

    iface.launch()

        
if __name__ == "__main__":
    main()

