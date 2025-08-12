# from unusedCurrently.wikipediaScraper import *
# from datasets import load_dataset
from researchPaperReader import *
# nltk.download()  # Download once; you can comment this out after first run

def main():

    # Example Call:
    # python run.py [link to research paper] [outputName]
    # Example call: python run.py "https://arxiv.org/pdf/1706.03762" "AttentionIsAllYouNeed"
    arguments = sys.argv[1:]
    url = arguments[0]
    outputName = arguments[1]

    researchPaper = extractTextFromPdfUrl(url)
    links = arxivReferencesToLinks(researchPaper)
    researchPaper = removeReferences(researchPaper)
    researchPaper = removeFormulas(researchPaper)
    researchPaper = removePaddings(researchPaper)
    with open(f"{outputName}.txt", "w") as f:
        f.write(researchPaper)
    print(links)
if __name__ == "__main__":
    main()

