import pandas as pd
import numpy as np
import os

def main():
  
    #data loading
    file_path="data/trends_clean.csv"

    if not os.path.exists(file_path):
        print("Clean CSV file not found. Run Task 2 first.")
        return

    df = pd.read_csv(file_path)

    print(f"Loaded data: {df.shape}\n")
    print("First 5 rows:")
    print(df.head(),"\n")

    #average calculations using Pandas
    avg_score=df["score"].mean()               #average score
    avg_comments=df["num_comments"].mean()     #average number of comments

    print(f"Average score   : {avg_score:.0f}")
    print(f"Average comments: {avg_comments:.0f}\n")

    #numpy analysis
    print("--- NumPy Stats ---")

    scores=df["score"].to_numpy()   

    #calculating stats of Score using numpy
    mean_score=np.mean(scores)                 #mean score
    median_score=np.median(scores)             #median score
    std_score=np.std(scores)                   #standard deviation
    max_score=np.max(scores)                   #maximum score
    min_score=np.min(scores)                   #minimum score

    print(f"Mean score   :{mean_score:.0f}")
    print(f"Median score :{median_score:.0f}")
    print(f"Std deviation:{std_score:.0f}")
    print(f"Max score    :{max_score:.0f}")
    print(f"Min score    :{min_score:.0f}\n")

    #Category analysis
    #finding category with highest number of stories
    category_counts=df["category"].value_counts()
    top_category=category_counts.idxmax()
    top_count=category_counts.max()

    print(f"Most stories in: {top_category} ({top_count} stories)\n")

    #story with most comments
    max_comments_idx=df["num_comments"].idxmax()
    top_story=df.loc[max_comments_idx]

    print(f'Most commented story: "{top_story["title"]}" — {top_story["num_comments"]} comments\n')

    
    #adding new columns for engagement and popularity
    #engagement = comments per score (normalized)
    df["engagement"]=df["num_comments"]/(df["score"] + 1)

    #marking stories as popular if above average score
    df["is_popular"]=df["score"]>avg_score

    
    #saving the data
    output_path="data/trends_analysed.csv"
    df.to_csv(output_path,index=False)
    print(f"Saved to {output_path}")


if __name__=="__main__":
    main()