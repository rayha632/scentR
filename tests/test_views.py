from unittest.mock import Mock

import pytest
from django.urls import reverse

from perfumes.models import Perfume

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_perfume():
    return Perfume.objects.create(
        id="creed-aventus",
        name="Aventus",
        house="Creed",
        family="Orchard Fruit",
        secondary_family="Wood & Root",
        description="A fruity, woody fragrance.",
        notes=["Pineapple", "Musk", "Bergamot"],
        top_notes=["Bergamot"],
        heart_notes=["Pineapple"],
        base_notes=["Musk"],
    )


def test_search_by_name(client, sample_perfume):
    response = client.get(
        reverse("perfume-search"),
        {"q": "aventus"},
    )

    assert response.status_code == 200
    assert b"Aventus" in response.content
    assert b"Creed" in response.content


def test_search_by_house(client, sample_perfume):
    response = client.get(
        reverse("perfume-search"),
        {"q": "creed"},
    )

    assert response.status_code == 200
    assert b"Aventus" in response.content


def test_search_no_matches(client, sample_perfume):
    response = client.get(
        reverse("perfume-search"),
        {"q": "nonexistent-fragrance"},
    )

    assert response.status_code == 200
    assert list(response.context["perfumes"]) == []


@pytest.fixture
def mock_recommender(monkeypatch):
    fake = Mock(
        return_value=[
            {
                "id": "similar-perfume",
                "name": "Similar Perfume",
                "house": "Test House",
                "similarity": 0.85,
            }
        ]
    )

    monkeypatch.setattr(
        "perfumes.views.get_similar_perfumes",
        fake,
    )

    return fake


def test_perfume_detail(client, sample_perfume, mock_recommender):
    response = client.get(
        reverse(
            "perfume-detail",
            args=[sample_perfume.id],
        )
    )

    assert response.status_code == 200
    assert b"Aventus" in response.content
    assert b"Pineapple" in response.content
    assert b"Similar Perfume" in response.content


def test_unknown_perfume_returns_404(client, sample_perfume):
    response = client.get(
        reverse(
            "perfume-detail",
            args=["does-not-exist"],
        )
    )

    assert response.status_code == 404


def test_default_algorithm(client, sample_perfume, mock_recommender):
    client.get(reverse("perfume-detail", args=[sample_perfume.id]))

    mock_recommender.assert_called_once_with(
        sample_perfume.id,
        algorithm="tfidf",
        top_n=5,
    )


def test_jaccard_algorithm(client, sample_perfume, mock_recommender):
    client.get(
        reverse("perfume-detail", args=[sample_perfume.id]),
        {"algorithm": "jaccard"},
    )

    mock_recommender.assert_called_once_with(
        sample_perfume.id,
        algorithm="jaccard",
        top_n=5,
    )


def test_invalid_algorithm(client, sample_perfume, mock_recommender):
    client.get(
        reverse("perfume-detail", args=[sample_perfume.id]),
        {"algorithm": "invalid"},
    )

    mock_recommender.assert_called_once_with(
        sample_perfume.id,
        algorithm="tfidf",
        top_n=5,
    )
