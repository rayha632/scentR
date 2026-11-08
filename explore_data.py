import pandas as pd

df = pd.read_json("data/perfumes.jsonl", lines=True)

print("Dataset Shape: ", df.shape)

print("\nColumns: ")
print(df.columns.tolist())

print("\nSample perfumes: ")
print(
    df[
        [
            "name",
            "house",
            "family",
            "character",
            "top_notes",
            "heart_notes",
            "base_notes",
        ]
    ].head()
)

print("\nDuplicate IDs: ", df["id"].duplicated().sum())

print("\nSample perfume details:")

print(
    df[
        [
            "name",
            "house",
            "family",
            "character",
            "top_notes",
            "heart_notes",
            "base_notes",
        ]
    ]
    .head(5)
    .to_string(index=False)
)

# Count perfumes with missing notes
missing_notes = df["notes"].apply(lambda x: len(x) == 0).sum()

print(f"Perfumes with no notes: {missing_notes}")

# Check completness of note pyramids
for column in ["top_notes", "heart_notes", "base_notes"]:
    missing = df[column].apply(lambda x: len(x) == 0).sum()

    print(f"{column}: {missing} empty entries")


# how many perfumes have a complete pyramid
complete_pyramids = df.apply(
    lambda row: all(
        len(row[col]) > 0 for col in ["top_notes", "heart_notes", "base_notes"]
    ),
    axis=1,
).sum()


print(f"Complete note pyramids: {complete_pyramids}")

# Inspect fragrance family distribution
print("\nMost common fragrance families:")
print(df["family"].value_counts().head(10))


# Select perfumes with at least one empty pyramid layer
incomplete = df[
    df[["top_notes", "heart_notes", "base_notes"]].apply(
        lambda row: any(len(notes) == 0 for notes in row), axis=1
    )
]

print("Incomplete pyramids:", len(incomplete))

print(
    incomplete[["name", "house", "notes", "top_notes", "heart_notes", "base_notes"]]
    .head(10)
    .to_string(index=False)
)
