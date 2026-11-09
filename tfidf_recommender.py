import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalise_notes(notes):
    return sorted({note.strip().casefold() for note in notes if note.strip()})


def build_tfidf_matrix(df):
    vectoriser = TfidfVectorizer(  # smoothed IDF
        analyzer=normalise_notes, binary=True
    )

    matrix = vectoriser.fit_transform(df["notes"].tolist())

    return vectoriser, matrix


def recommend_tfidf(df, matrix, perfume_id, top_n=5):
    ids = df["id"].tolist()

    if perfume_id not in ids:
        raise ValueError(f"Perfume '{perfume_id}' not found")

    target_pos = ids.index(perfume_id)

    # calculate cosine similarity
    similarities = cosine_similarity(matrix[target_pos], matrix).flatten()

    scores = []

    for i, row in enumerate(df.itertuples(index=False)):
        if i == target_pos:
            continue  # exlude original

        scores.append(
            {
                "id": row.id,
                "name": row.name,
                "house": row.house,
                "similarity": float(similarities[i]),
            }
        )

        # sort based on similarity in decreasing order, hey guys welcome to top 10 mr beast perfume
        scores.sort(key=lambda item: item["similarity"], reverse=True)

    return scores[:top_n]


if __name__ == "__main__":
    df = pd.read_json("data/perfumes.jsonl", lines=True)

    vectorizer, matrix = build_tfidf_matrix(df)

    print("Matrix shape:", matrix.shape)

    # Compare the first perfume against every perfume
    similarities = cosine_similarity(matrix[0], matrix)

    print(similarities.shape)
    print(similarities[0][:10])

    recommendations = recommend_tfidf(df, matrix, "creed-aventus", top_n=5)

    print("TF-IDF recommendations for Creed Aventus:")

    for perfume in recommendations:
        print(f"{perfume['house']} {perfume['name']}: {perfume['similarity']:.3f}")

    test_ids = [
        "tom-ford-oud-wood",
        "mfk-baccarat-rouge-540",
        "parfums-de-marly-layton",
        "kilian-angels-share",
        "ysl-libre",
    ]

    for perfume_id in test_ids:
        print(f"\nRecommendations for {perfume_id}:")

        recommendations = recommend_tfidf(df, matrix, perfume_id, top_n=5)

        for perfume in recommendations:
            print(f"  {perfume['name']}: {perfume['similarity']:.3f}")
