import fitz  # PyMuPDF
import sys
from transformers import GPT2Tokenizer, GPT2Model, pipeline
from nltk.tokenize import sent_tokenize
import torch

# input: pdf: researchPaper
# output: string of researchPaper
def extractTextPymupdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# input: researchPaper as string
# output: researchPaper as string, with references removed
def removeReferences(researchPaper: str):
    researchPaper = extractTextPymupdf("BRIC.pdf")
    arrayOfWords = researchPaper.split()
    for index, word in enumerate(arrayOfWords):
        if word == "REFERENCES":
            arrayOfWords = arrayOfWords[0:index]
            break

    researchPaper = " ".join(arrayOfWords)
    return researchPaper

#input: research Paper text in string form
def gpt2Tokenize(text: str):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return tokenizer.encode(text)

# takes in list of tokens
def chunkAndPadTokens(tokens, max_length, pad_token_id=0):
    chunks = []
    # Split tokens into chunks of max_length
    for i in range(0, len(tokens), max_length):
        chunk = tokens[i:i+max_length]
        # Pad the last chunk if needed
        if len(chunk) < max_length:
            padding_length = max_length - len(chunk)
            chunk = chunk + [pad_token_id] * padding_length
        chunks.append(chunk)
    return chunks


# finds relationships between words
#input shape : (x,1024)
def getGPT2Embeddings(token_ids_batch: torch.Tensor) -> torch.Tensor:
    """
    Loads GPT-2, embeds the token ID batch.

    Args:
        token_ids_batch (torch.Tensor): shape [batch_size, seq_len]

    Returns:
        torch.Tensor: shape [batch_size, seq_len, embedding_dim]
    """
    model = GPT2Model.from_pretrained("gpt2")
    model.eval()
    
    with torch.no_grad():
        outputs = model(token_ids_batch)
        embeddings = outputs.last_hidden_state
    return embeddings