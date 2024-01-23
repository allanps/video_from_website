print("hello world")

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np
from transformers import pipeline

# Function to extract and preprocess website content
def extract_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = ' '.join([p.text for p in soup.find_all('p')])
    return text

# Function to extract themes using NMF (Non-negative Matrix Factorization)
def extract_themes(preprocessed_content, n_topics=5):
    # Since we're dealing with a single document, we can set min_df to 1 and max_df to a high number to avoid the error.
    vectorizer = TfidfVectorizer(max_df=1.0, min_df=1, stop_words='english')
    tfidf = vectorizer.fit_transform([preprocessed_content])
    nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
    feature_names = vectorizer.get_feature_names_out()
    themes = []
    for topic_idx, topic in enumerate(nmf.components_):
        themes.append(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))
    return themes

# Function to generate transcript segments
def generate_transcript_dummy(themes, n):
    segments = []
    for i in range(n):
        # Ensure coherent segments by using one theme at a time.
        selected_theme = np.random.choice(themes)
        segments.append(selected_theme)
    return segments

def generate_transcript(theme, n_sequences=3):
    gpt2_generator = pipeline('text-generation', model='gpt2')
    
    sentences = gpt2_generator(
        theme,
        do_sample=True,
        top_k=50,
        temperature=0.6,
        max_length=128,
    num_return_sequences=n_sequences
    )

    return sentences

if __name__ == "__main__":

    # Example usage
    # url = 'https://motorola.com/'
    url = 'https://databricks.com/'
    preprocessed_content = extract_content(url)
    print(preprocessed_content)
    themes = extract_themes(preprocessed_content)
    segments = generate_transcript(themes[0], 5)

    for segment in segments:
        print("\n New segment: \n")
        print(segment["generated_text"])


