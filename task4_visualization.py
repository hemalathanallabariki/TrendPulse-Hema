import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#shortening long titles for charts
def shorten_title(title, max_length=50):
    return title if len(title)<=max_length else title[:47] + "..."

def main():
    #path to analysed csv from Task 3
    file_path="data/trends_analysed.csv"
    #checking if file exists
    if not os.path.exists(file_path):
        print("Analysed CSV not found. Run Task 3 first.")
        return

    df=pd.read_csv(file_path)

    #create outputs folder if not exists
    if not os.path.exists("outputs"):
        os.makedirs("outputs")


#CHART 1: Top 10 stories by score
    #getting top 10 stories based on score
    top10=df.sort_values(by="score",ascending=False).head(10)
    plt.figure()
    
    plt.barh(
        [shorten_title(t) for t in top10["title"]],
        top10["score"]
    )
    #labels and title
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    #highest on top
    plt.gca().invert_yaxis()  
    #adjust layout and save
    plt.tight_layout()
    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()




#CHART 2: Number of stories per category

    #counting number of stories in each category
    category_counts=df["category"].value_counts()

    #using default color map
    colors=plt.cm.tab10(np.arange(len(category_counts)))
    plt.figure()
    plt.bar(category_counts.index,category_counts.values,color=colors)
    #labels and title
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")
    #adjust layout and save
    plt.tight_layout()
    plt.savefig("outputs/chart2_categories.png")
    plt.close()



#CHART 3: Scatter plot of Score vs Number of Comments

    plt.figure()
    #separating popular and non-popular stories
    popular=df[df["is_popular"]==True]
    not_popular=df[df["is_popular"]==False]
    #plotting popular and not popular with different colors
    plt.scatter(popular["score"],popular["num_comments"],label="Popular",color="green")
    plt.scatter(not_popular["score"],not_popular["num_comments"],label="Not Popular",color="red")
    #labels and title
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()
    #adjust layout and save
    plt.tight_layout()
    plt.savefig("outputs/chart3_scatter.png")
    plt.close()



    # -------------------------------
    # Bonus: Dashboard (combining all charts)
    # -------------------------------
    fig,axes=plt.subplots(1,3,figsize=(18, 5))

    # Chart 1 in dashboard
    axes[0].barh(
        [shorten_title(t) for t in top10["title"]],
        top10["score"]
    )
    axes[0].set_title("Top Stories")
    axes[0].invert_yaxis()

    # Chart 2 in dashboard
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Categories")

    # Chart 3 in dashboard
    axes[2].scatter(popular["score"],popular["num_comments"],label="Popular")
    axes[2].scatter(not_popular["score"],not_popular["num_comments"],label="Not Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard")

    plt.tight_layout()
    plt.savefig("outputs/dashboard.png")
    plt.close()

    print("Charts saved in outputs/ folder.")


if __name__=="__main__":
    main()