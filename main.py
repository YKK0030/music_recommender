import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import nltk
nltk.download('punkt')

# Read the dataset
df = pd.read_csv("spotify_millsongdata.csv")

# Sample 5000 rows and drop the 'link' column
df = df.sample(5000).drop('link', axis=1).reset_index(drop=True)

# Preprocess the text data
df['text'] = df['text'].str.lower().replace(r'^\w\s', ' ').replace(r'\n', ' ', regex=True)

# Tokenization and stemming
import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenization(txt):
    tokens = nltk.word_tokenize(txt)
    stemming = [stemmer.stem(w) for w in tokens]
    return " ".join(stemming)

df['text'] = df['text'].apply(lambda x: tokenization(x))

# TF-IDF Vectorization
tfidvector = TfidfVectorizer(analyzer='word', stop_words='english')
matrix = tfidvector.fit_transform(df['text'])

# Calculate cosine similarity
similarity = cosine_similarity(matrix)

# Function to recommend similar songs
def recommendation(song_title):
    # Check if the song exists in the DataFrame
    if song_title not in df['song'].values:
        print(f"Song '{song_title}' not found in the dataset.")
        return []

    # Get the index of the song in the DataFrame
    idx = df[df['song'] == song_title].index[0]

    # Calculate distances and find similar songs
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    songs = [df.iloc[m_id[0]].song for m_id in distances[1:21]]  # Exclude the song itself
    return songs

# Test the recommendation function
song_to_recommend = 'Crying Over You'
recommended_songs = recommendation(song_to_recommend)
print(f"\nSongs similar to '{song_to_recommend}':")
print(recommended_songs)

# Save similarity matrix and preprocessed DataFrame to files using pickle
pickle.dump(similarity, open('similarity.pkl', 'wb'))
pickle.dump(df, open('df.pkl', 'wb'))
