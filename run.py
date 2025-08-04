from wikipediaScraper import *
# from datasets import load_dataset
from pdfReaderCleaner import *
# nltk.download()  # Download once; you can comment this out after first run

def main():

    pages = returnCleanedTextOfAllArticles("minecraft")
    pages = " ".join(pages)  # joins with spaces between

    print(len(pages))

    # Example Call:
    # python run.py [relative path to pdf] [outputName]
    # python run.py "BRIC.pdf" "BRIC"
    # arguments = sys.argv[1:]
    # researchPaper = arguments[0]
    # work on making a gpt2 tokenizer, and generating questions from that.
    # researchPaper = extractTextPymupdf(researchPaper)
    # researchPaper = removeReferences(researchPaper)
    # researchPaperTokenized = gpt2Tokenize(researchPaper)
    # batchedTokens = torch.tensor(chunkAndPadTokens(researchPaperTokenized,1024,0))
    # researchPaperEmbeddings = getGPT2Embeddings(batchedTokens)
    # chunkedEmbeddings = chunkEmbeddings(researchPaperEmbeddings)
    # print(chunkedEmbeddings.shape)
if __name__ == "__main__":
    main()

