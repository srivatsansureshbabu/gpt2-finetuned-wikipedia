# gpt2-research-assistant

Work-in-progress NLP pipeline for fine-tuning GPT-2 on selectively scraped Wikipedia content.

## Current Milestones
- Scraped machine learning text from Wikipedia and cleaned it  
- Created question-answer generation prompts using a QG transformer model  
- Accelerated QG transformer model inference by 9X using GPU  
- Fed data into GPT-2 model and experimented with fine-tuning  

## File Information
- **run.py** — Main script  
- **wikipediaScraper.py** — Functions for scraping and cleaning Wikipedia text  
- **pdfReaderCleaner.py** — Placeholder for future research paper analysis  
- **fineTuningGPT.ipynb** — Notebook for model generation (recommended to run in Google Colab with GPU)  

## Data
- **BRIC.pdf** — Research paper on machine learning  
- **BRIC.txt** — Extracted and cleaned data from research paper  
- **cleanedMachineLearningText.txt** — Machine learning text scraped from Wikipedia  
- **metrics.txt** — Tracking speedups and efficiency  

## How to Run

```bash
# Download all independencies
pip install -r requirements.txt
```

```bash
# Generates cleanedMachineLearningText.txt
python run.py
```

## How to Run

1. **Download the Data**  
   Ensure you have the cleaned `.txt` data file ready for fine-tuning.

2. **Download the Notebook**  
   Download `generateQuestions.ipynb` from the repository. This notebook handles the question generation that we feed into our model.

3. **Open in Google Colab**  
   Upload `cleanedMachineLearningText.txt` and `generateQuestions.ipynb` to Google Drive and open `generateQuestions.ipynb` in [Google Colab](https://colab.research.google.com/).  
   - Recommended for free GPU access to speed up fine-tuning.  
   - Enable GPU by going to:  
     `Runtime` > `Change runtime type` > select `GPU` > Save.


