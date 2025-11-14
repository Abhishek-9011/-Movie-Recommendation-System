import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns
import ast

credits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.read_csv('tmdb_5000_movies.csv')

# print(credits.isnull().sum())
# print('------------------------------------------')
# print(movies.isnull().sum())

movies = movies.merge(credits, on='title')
# print('-----------------------------------')
# print(movies.shape)
# print(movies.columns.tolist())  
# print(movies.isnull().sum())

cols_to_drop = ['homepage', 'status', 'original_title']

for c in cols_to_drop:
    if c in movies.columns:
        movies.drop(columns=[c], inplace=True)

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]


def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

def convert_cast(text):
    L = []
    for i in ast.literal_eval(text):
        if len(L) < 3:
            L.append(i['name'])
    return L

movies['cast'] = movies['cast'].apply(convert_cast)

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].fillna('')
movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "").lower() for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "").lower() for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "").lower() for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "").lower() for i in x])

movies['tags'] = (
    movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
)

# print(movies)


new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# print(new_df)

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# print(vectors.shape)  # (number_of_movies, 5000)


pca = PCA(n_components=2)
reduced_vectors = pca.fit_transform(vectors)

# print("Reduced shape:", reduced_vectors.shape)
# plt.figure(figsize=(10,6))
# sns.scatterplot(x=reduced_vectors[:,0], y=reduced_vectors[:,1], s=20, color="green")
# plt.title("Movies represented in 2D PCA Space")
# plt.xlabel("Principal Component 1")
# plt.ylabel("Principal Component 2")
# plt.show()

model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(vectors)

def recommend_knn(movie):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        print("Movie not found in dataset.")
        return

    index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances, indices = model_knn.kneighbors([vectors[index]], n_neighbors=6)

    print(f"\n🎥 Recommendations for '{new_df.iloc[index].title}':")
    for i in indices[0][1:]:
        print(new_df.iloc[i].title)
def get_recommendations(movie_name):
    movie_name = movie_name.lower()
    if movie_name not in new_df['title'].str.lower().values:
        return {"error": "Movie not found in dataset."}

    index = new_df[new_df['title'].str.lower() == movie_name].index[0]
    distances, indices = model_knn.kneighbors([vectors[index]], n_neighbors=6)

    recommendations = []
    for i in indices[0][1:]:
        recommendations.append(new_df.iloc[i].title)
    return {"recommendations": recommendations}

# recommend_knn("Avatar")
