from functools import lru_cache

import pandas as pd

from recommender import recommend_similar
from tfidf_recommender import build_tfidf_matrix, recommend_tfidf

from .models import Perfume


@lru_cache(maxsize=1)
def get_recommender_data():
    # Retrieve perfumes in consistent order
    records = list(
        Perfume.objects.order_by("id").values("id", "name", "house", "notes")
    )

    # convert SQL records into a DataFrame
    df = pd.DataFrame.from_records(records, columns=["id", "name", "house", "notes"])

    if df.empty:
        return df, None

    # Build TF-IDF Matrix
    _, matrix = build_tfidf_matrix(df)

    return df, matrix


def get_similar_perfumes(perfume_id, algorithm="tfidf", top_n=5):
    df, matrix = get_recommender_data()

    if df.empty:
        return []

    if algorithm == "jaccard":
        return recommend_similar(df, perfume_id, top_n)

    if algorithm == "tfidf":
        return recommend_tfidf(df, matrix, perfume_id, top_n)

    raise ValueError(f"Unknown algorithm: {algorithm}")
