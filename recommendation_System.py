import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Load Dataset ---
# A small movie dataset (title + description). You can expand it.
data = {
    "title": [
        "Inception",
        "The Dark Knight",
        "Interstellar",
        "The Matrix",
        "The Prestige",
        "Avengers: Endgame",
        "Iron Man",
        "Doctor Strange",
        "Shutter Island",
        "Tenet"
    ],
    "description": [
        "A thief who steals corporate secrets through dream-sharing technology.",
        "Batman faces the Joker, a criminal mastermind wreaking havoc on Gotham.",
        "A team travels through a wormhole in space in search of a new home for humanity.",
        "A hacker discovers the reality is a simulation and fights against machines.",
        "Two magicians engage in a battle to create the ultimate stage illusion.",
        "Avengers assemble one last time to undo Thanos’ snap and save the universe.",
        "A billionaire builds a high-tech suit and becomes the superhero Iron Man.",
        "A surgeon learns mystic arts to protect the world from magical threats.",
        "A US marshal investigates a psychiatric facility and its hidden secrets.",
        "A secret agent manipulates time to prevent World War III."
    ]
}

df = pd.DataFrame(data)

# --- Feature Extraction ---
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["description"])

# --- Cosine Similarity ---
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


def recommend(movie_title, n=5):
    """Recommend n similar movies to the given movie title (case-insensitive)."""
    # Match case-insensitive
    matches = df[df["title"].str.lower() == movie_title.lower()]
    if matches.empty:
        return f"❌ Movie '{movie_title}' not found in dataset."

    idx = matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1 : n + 1]  # exclude the movie itself

    recommendations = [df["title"].iloc[i] for i, _ in sim_scores]
    return recommendations


# --- Demo Run ---
if _name_ == "_main_":
    print("🎬 Movie Recommendation System")
    print("Available movies:", ", ".join(df["title"].values))
    movie = input("Enter a movie you like: ").strip()
    recs = recommend(movie, n=3)
    if isinstance(recs, list):
        print("\n✅ Recommended movies for you:")
        for r in recs:
            print(" -", r)
    else:
        print(recs)