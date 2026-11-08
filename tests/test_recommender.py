import pandas as pd
import pytest

from recommender import jaccard_similarity, recommend_similar


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


def test_identical_notes():
    a = ["Vanilla", "Musk"]
    b = ["Vanilla", "Musk"]

    assert jaccard_similarity(a, b) == 1.0


def test_disjoint_notes():
    a = ["Vanilla", "Musk"]
    b = ["Oud", "Rose"]

    assert jaccard_similarity(a, b) == 0.0


def test_partial_overlap():
    a = ["Vanilla", "Musk", "Bergamot"]
    b = ["Vanilla", "Musk", "Amber"]

    assert jaccard_similarity(a, b) == 0.5


def test_empty_notes():
    assert jaccard_similarity([], []) == 0.0


def test_normalisation_and_duplicates():
    a = [" Vanilla ", "MUSK", "Musk"]
    b = ["vanilla", "musk"]

    assert jaccard_similarity(a, b) == 1.0


def test_excludes_original(sample_perfumes):
    results = recommend_similar(sample_perfumes, "target", top_n=3)

    assert all(p["id"] != "target" for p in results)


def test_returns_top_n(sample_perfumes):
    results = recommend_similar(sample_perfumes, "target", top_n=2)

    assert len(results) == 2


def test_unknown_perfume(sample_perfumes):
    with pytest.raises(ValueError):
        recommend_similar(sample_perfumes, "unknown")


def test_recommendation_order(sample_perfumes):
    results = recommend_similar(sample_perfumes, "target", top_n=3)

    ids = [perfume["id"] for perfume in results]

    assert ids == ["closest", "partial", "unrelated"]
