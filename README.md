# gpt2-research-assistant

Work-in-progress NLP pipeline for fine-tuning GPT-2 on selectively scraped Wikipedia content.

## Current Milestones
- Currently read and cleaned research papers
- Extracted reference links  

## File Information
- **run.py** — Main script  
- **researchPaperReader.py** — reads research papers  
- **fineTuningGPT.ipynb** — Notebook for model generation (recommended to run in Google Colab with GPU)  

## Data
- **metrics.txt** — Tracking speedups and efficiency  

## How to Run

```bash
# Download all independencies
pip install -r requirements.txt
```

```bash
# Example Call:
# python run.py [link to research paper] [outputName]
# Example call: 
python run.py "https://arxiv.org/pdf/1706.03762" "AttentionIsAllYouNeed"
```


