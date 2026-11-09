import pandas as pd
import pytest
from sklearn.metrics.pairwise import cosine_similarity

from tfidf_recommender import (
    build_tfidf_matrix,
    recommend_tfidf,
)


@pytest.fixture
def sample_perfumes():
    return pd.DataFrame(
        [
            {
                "id": "target",
                "name": "Target",
                "house": "House A",
                "notes": ["Vanilla", "Musk"],
            },
            {
                "id": "closest",
                "name": "Closest",
                "house": "House B",
                "notes": ["Vanilla", "Musk"],
            },
            {
                "id": "partial",
                "name": "Partial",
                "house": "House C",
                "notes": ["Vanilla", "Amber"],
            },
            {
                "id": "unrelated",
                "name": "Unrelated",
                "house": "House D",
                "notes": ["Oud"],
            },
        ]
    )


def test_tfidf_matrix_shape(sample_perfumes):
    vectoriser, matrix = build_tfidf_matrix(sample_perfumes)

    assert matrix.shape == (4, 4)

    assert set(vectoriser.get_feature_names_out()) == {
        "vanilla",
        "musk",
        "amber",
        "oud",
    }


def test_tfidf_normalisation():
    df = pd.DataFrame(
        {
            "notes": [
                [" Vanilla ", "MUSK", "Musk"],
                ["vanilla", "musk"],
                ["Black Pepper"],
            ]
        }
    )

    vectoriser, matrix = build_tfidf_matrix(df)

    assert set(vectoriser.get_feature_names_out()) == {
        "vanilla",
        "musk",
        "black pepper",
    }

    similarity = cosine_similarity(matrix[0], matrix[1])[0, 0]

    assert similarity == pytest.approx(1.0)


def test_rare_notes_have_higher_idf(sample_perfumes):
    vectoriser, _ = build_tfidf_matrix(sample_perfumes)

    vocabulary = vectoriser.vocabulary_
    idf = vectoriser.idf_

    vanilla_idf = idf[vocabulary["vanilla"]]
    oud_idf = idf[vocabulary["oud"]]

    assert oud_idf > vanilla_idf


def test_identical_perfumes_cosine(sample_perfumes):
    _, matrix = build_tfidf_matrix(sample_perfumes)

    score = cosine_similarity(matrix[0], matrix[1])[0, 0]

    assert score == pytest.approx(1.0)


def test_disjoint_perfumes_cosine(sample_perfumes):
    _, matrix = build_tfidf_matrix(sample_perfumes)

    score = cosine_similarity(matrix[0], matrix[3])[0, 0]

    assert score == pytest.approx(0.0)


def test_tfidf_recommendation_order(sample_perfumes):
    _, matrix = build_tfidf_matrix(sample_perfumes)

    results = recommend_tfidf(sample_perfumes, matrix, "target", top_n=3)

    ids = [perfume["id"] for perfume in results]

    assert ids == ["closest", "partial", "unrelated"]


def test_tfidf_excludes_original(sample_perfumes):
    _, matrix = build_tfidf_matrix(sample_perfumes)

    results = recommend_tfidf(sample_perfumes, matrix, "target", top_n=3)

    assert all(p["id"] != "target" for p in results)


def test_tfidf_top_n(sample_perfumes):
    _, matrix = build_tfidf_matrix(sample_perfumes)

    results = recommend_tfidf(sample_perfumes, matrix, "target", top_n=2)

    assert len(results) == 2


def test_tfidf_unknown_perfume(sample_perfumes):
    _, matrix = build_tfidf_matrix(sample_perfumes)

    with pytest.raises(ValueError):
        recommend_tfidf(sample_perfumes, matrix, "does-not-exist")


def test_tfidf_nondefault_dataframe_index(sample_perfumes):
    df = sample_perfumes.copy()
    df.index = [10, 20, 30, 40]

    _, matrix = build_tfidf_matrix(df)

    results = recommend_tfidf(df, matrix, "target", top_n=3)

    assert [p["id"] for p in results] == ["closest", "partial", "unrelated"]
