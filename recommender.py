import pandas as pd

def jaccard_similarity(notes_a, notes_b):
    # Normalize note names and remove duplicates
    a = {note.strip().casefold() for note in notes_a}
    b = {note.strip().casefold() for note in notes_b}

    union = a | b
    intersection = a & b

    if not union:
        return 0.0

    return len(intersection) / len(union)

print(jaccard_similarity(
    ["Vanilla", "Musk", "Bergamot"],
    ["Vanilla", "Musk", "Amber"]
))


def recommend_similar(df, perfume_id, top_n=5):

    #find matching perfume to id
    matches = df[df["id"] == perfume_id]

    if matches.empty:
        raise ValueError(f"Perfume '{perfume_id}' not found")

    matching_perfume = matches.iloc[0]

    #extract target notes
    target_notes = matching_perfume["notes"]

    scores = []

    #compare target notes with all other perfumes
    for _, row in df.iterrows():
        score = jaccard_similarity(target_notes, row["notes"])

        scores.append({
            "id": row["id"],
            "name": row["name"],
            "house": row["house"],
            "similarity": score
        })

        #exclude original perfume
        scores = [
            item for item in scores
            if item["id"] != perfume_id
        ]

        scores.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

    return scores[:top_n]


if __name__ == "__main__":
    df = pd.read_json("data/perfumes.jsonl", lines=True)

    recommendations = recommend_similar(
        df, "creed-aventus", top_n=5
    )


    for perfume in recommendations:
        print(
            f"{perfume['house']} {perfume['name']}: "
            f"{perfume['similarity']:.3f}"
        )