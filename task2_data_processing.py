import pandas as pd
import os
from datetime import datetime

def main():
    #find latest JSON file in data folder
    data_folder="data"
    #list all files in the data folder that match the pattern "trends_*.json"
    files=[f for f in os.listdir(data_folder) if f.startswith("trends_") and f.endswith(".json")]

    if not files:
        print("No JSON file found in data/ folder.")
        return

    #latest file
    files.sort(reverse=True)
    latest_file=os.path.join(data_folder, files[0])

    df = pd.read_json(latest_file)
    
    print(f"Loaded {len(df)} stories from {latest_file}\n")

    #removing duplicate stories
    before=len(df)
    df=df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    #removing rows with missing important values
    df=df.dropna(subset=["post_id","title","score"])
    print(f"After removing nulls: {len(df)}")

    #converting score and comments to integer
    df["score"]=df["score"].astype(int)
    df["num_comments"]=df["num_comments"].astype(int)

    #removing low quality stories
    df=df[df["score"]>=5]
    print(f"After removing low scores: {len(df)}")

    #Cleaning extraspaces in titles
    df["title"]=df["title"].str.strip()

    #saving cleaned data
    output_file=os.path.join(data_folder,"trends_clean.csv")

    df.to_csv(output_file, index=False)

    print(f"\nSaved {len(df)} rows to {output_file}\n")

    
    #Summary of categories
    print("Stories per category:")
    category_counts=df["category"].value_counts()
    for category,count in category_counts.items():
        print(f" {category} \t {count}")


if __name__=="__main__":
    main()