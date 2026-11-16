
# ScentR — Perfume Recommendation System

A full stack web application that helps users discover fragrances similar to their favourites using simple recommendation algorithms.

**[Live Demo](https://scentr.onrender.com/)**

## Features

- Search a catalogue of 1,479 perfumes by name or fragrance house.
- Explore fragrance profiles, notes, and scent characteristics.
- Discover similar perfumes using two recommendation algorithms:
  - **Jaccard Similarity:** Measures overlap between fragrance notes.
  - **TF-IDF + Cosine Similarity:** Weights notes by their relative rarity to identify meaningful similarities.
- Compare recommendations by switching between algorithms.

## Tech Stack

| Component | Technologies |
|---|---|
| Backend | Python, Django |
| Database | PostgreSQL |
| Recommendation Engine | scikit-learn, pandas, NumPy |
| Frontend | HTML, CSS, Django Templates |
| Deployment | Render, Neon, Gunicorn, WhiteNoise |
| Testing & CI/CD | pytest, GitHub Actions, Ruff |

## Data Attribution

Fragrance data sourced from the [Scento Perfume Database](https://www.scento.com/perfume-database).

## Notes and Future Improvements

- Recommendation algorithms: The current algorithms are relatively simple and could be extended to provide more nuanced, expressive, and personalised recommendations.

- Dataset limitations: The relatively small dataset (covers mostly mainstream fragrances) limits the variety and coverage of recommendations, especially for more obscure fragrances. A large niche brand won't copy another large niche brand for example, so trying to find its similar counterpart/dupe will require larger datasets from sites like Fragrantica. 


