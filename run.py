from wikipediaScraper import *
# from datasets import load_dataset
from pdfReaderCleaner import *
# nltk.download()  # Download once; you can comment this out after first run

def main():
    allPages = []
    topics = [
    "Supervised Learning",
    "Unsupervised Learning",
    "Reinforcement Learning",
    "Neural Networks",
    # "Deep Learning",
    # "Convolutional Neural Networks",
    # "Recurrent Neural Networks",
    # "Long Short-Term Memory",
    # "Transformer Models",
    # "Natural Language Processing",
    # "Computer Vision",
    # "Generative Adversarial Networks",
    # "Autoencoders",
    # "Support Vector Machines",
    # "Decision Trees",
    # "Random Forests",
    # "Gradient Boosting",
    # "XGBoost",
    # "LightGBM",
    # "CatBoost",
    # "Clustering Algorithms",
    # "K-Means Clustering",
    # "Hierarchical Clustering",
    # "Dimensionality Reduction",
    # "Principal Component Analysis",
    # "t-SNE",
    # "Feature Engineering",
    # "Feature Selection",
    # "Model Evaluation Metrics",
    # "Cross-Validation",
    # "Overfitting and Underfitting",
    # "Regularization Techniques",
    # "Dropout",
    # "Batch Normalization",
    # "Optimization Algorithms",
    # "Stochastic Gradient Descent",
    # "Adam Optimizer",
    # "Learning Rate Scheduling",
    # "Hyperparameter Tuning",
    # "Transfer Learning",
    # "Ensemble Methods",
    # "Recommender Systems",
    # "Time Series Analysis",
    # "Anomaly Detection",
    # "Bayesian Methods",
    # "Markov Chains",
    # "Hidden Markov Models",
    # "Reinforcement Learning Algorithms",
    # "Q-Learning",
    # "Policy Gradient Methods",
    # "Deep Q-Networks",
    # "Ethics in AI",
    # "Explainable AI",
    # "AI Fairness",
    # "Data Augmentation",
    # "Data Preprocessing",
    # "Machine Learning Pipelines",
    # "AutoML",
    # "TensorFlow",
    # "PyTorch",
    # "Scikit-learn",
    # "Keras",
    # "CoreML",
    # "ONNX",
    # "ML Deployment",
    # "Model Interpretability",
    # "Federated Learning",
    # "Multi-task Learning",
    # "Self-supervised Learning",
    # "Contrastive Learning",
    # "Few-shot Learning",
    # "Zero-shot Learning",
]
    for topic in topics:
        pages = returnCleanedTextOfAllArticles(topic)

        pages = " ".join(pages)  # joins with spaces between
        allPages.append(pages)

    allArticles = " ".join(allPages)
    print(len(allArticles))
    with open("cleanedMachineLearningText.txt", "w", encoding="utf-8") as f:
        f.write(allArticles)

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

