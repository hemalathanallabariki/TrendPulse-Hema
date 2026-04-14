import pandas as pd
import os

# file paths
input_file = "data/trends_20260414.json"
output_file = "data/trends_clean.csv"


# check if file exists before loading
if not os.path.exists(input_file):
    print("file not found:", input_file)

else:
    # loading json data into dataframe
    data = pd.read_json(input_file)

    print(f"\nLoaded {len(data)} stories from {input_file}\n")


    # -------- cleaning steps -------- #

    # removing duplicate posts
    data = data.drop_duplicates(subset="post_id")
    print("After removing duplicates:", len(data))


    # removing rows with missing important values
    data = data.dropna(subset=["post_id", "title", "score"])
    print("After removing nulls:", len(data))


    # converting score and comments to numeric (in case of bad values)
    data["score"] = pd.to_numeric(data["score"], errors="coerce")
    data["num_comments"] = pd.to_numeric(data["num_comments"], errors="coerce")

    # dropping rows where conversion failed
    data = data.dropna(subset=["score", "num_comments"])

    # converting to int type
    data["score"] = data["score"].astype(int)
    data["num_comments"] = data["num_comments"].astype(int)


    # removing low score stories
    data = data[data["score"] >= 5]
    print("After removing low scores:", len(data))


    # cleaning extra spaces in title
    data["title"] = data["title"].str.strip()


    # -------- saving file -------- #

    os.makedirs("data", exist_ok=True)
    data.to_csv(output_file, index=False)

    print(f"\nSaved {len(data)} rows to {output_file}")


    # -------- summary -------- #

    print("\nStories per category:")

    counts = data["category"].value_counts()

    for cat in counts.index:
        print(f"  {cat}\t{counts[cat]}")