import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np

class Transcript:
    def __init__(self):
        pass

    # Function to extract and preprocess website content
    def extract_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ' '.join([p.text for p in soup.find_all('p')])
        return text

    # Function to extract themes using NMF (Non-negative Matrix Factorization)
    def extract_themes(self, preprocessed_content, n_topics=5):
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
    def generate_transcript(self, themes, n):
        segments = []
        for i in range(n):
            # Ensure coherent segments by using one theme at a time.
            selected_theme = np.random.choice(themes)
            segments.append(selected_theme)
        return segments

    # Function to generate transcript segments
    def run(self, url):
        preprocessed_content = self.extract_content(url)
        themes = self.extract_themes(preprocessed_content)
        segments = self.generate_transcript(themes, 5)
        return segments
