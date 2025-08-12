from io import BytesIO
import PyPDF2
import fitz  # PyMuPDF
import sys
from transformers import GPT2Tokenizer, GPT2Model, pipeline
from nltk.tokenize import sent_tokenize
import requests
import re
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
    arrayOfWords = researchPaper.split()
    for index, word in enumerate(arrayOfWords):
        if word == "REFERENCES":
            arrayOfWords = arrayOfWords[0:index]
            break

    researchPaper = " ".join(arrayOfWords)
    return researchPaper

import re

#input: researchPaper
#output: list of references
def arxivReferencesToLinks(referenceText: str) -> list[str]:
    # Regex to capture arXiv IDs, like arXiv:1607.06450 or abs/1607.06450
    arxiv_pattern = r'arXiv[: ]?(\d{4}\.\d{4,5}|\d{7})(v\d+)?'
    
    # Find all matches
    matches = re.findall(arxiv_pattern, referenceText, flags=re.IGNORECASE)
    
    # Extract the ID part only (first group)
    arxiv_ids = [match[0] for match in matches]
    
    # Create direct PDF links for each arXiv ID
    links = [f"https://arxiv.org/pdf/{arxiv_id}.pdf" for arxiv_id in arxiv_ids]
    
    # Remove duplicates just in case
    return list(set(links))

# input: researchPaper as string
# output: cleaned researchPaper as string without formulas, figures
def removeFormulas(text):
    # Remove lines with many +1, -1, 0 or similar patterns
    text = re.sub(r'^[\s\+\-\d]+$', '', text, flags=re.MULTILINE)

    # Remove figure/table captions (e.g., lines starting with 'Figure' or 'Table')
    text = re.sub(r'^(Figure|Table)\s*\d+.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)

    # Remove lines with mostly symbols or non-alpha characters
    text = re.sub(r'^[^\w\s]{5,}$', '', text, flags=re.MULTILINE)

    # Remove references like [9], [10], etc.
    text = re.sub(r'\[\d+\]', '', text)

    # Optionally remove very short lines (<10 chars)
    text = '\n'.join([line for line in text.split('\n') if len(line.strip()) > 10])

    return text

def extractTextFromPdfUrl(pdfUrl):
    response = requests.get(pdfUrl)
    response.raise_for_status()

    pdfFile = BytesIO(response.content)
    reader = PyPDF2.PdfReader(pdfFile)

    text = ""
    for page in reader.pages:
        pageText = page.extract_text()
        if pageText:
            text += pageText + "\n"
    return text

def removePaddings(text):
    """
    Removes <pad>, <EOS>, and extra spaces from the given text.
    """
    # Remove both <EOS> and <pad> with surrounding spaces
    cleaned = re.sub(r'\s*<(?:EOS|pad)>\s*', ' ', text)
    # Collapse multiple spaces into one
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned