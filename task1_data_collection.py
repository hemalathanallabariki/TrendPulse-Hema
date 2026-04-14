import requests
import time
import json
import os
from datetime import datetime

#base url for hackernews api
BASE_URL="https://hacker-news.firebaseio.com/v0"
HEADERS={"User-Agent": "TrendPulse/1.0"}

#limits for collection
MAX_PER_CATEGORY=25
TOTAL_IDS_TO_FETCH=500

#keywords for each category
CATEGORIES={
    "technology":["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews":["war","government","country","president","election","climate","attack","global"],
    "sports":["nfl","nba","fifa","sport","team","player","league","championship"],
    "science":["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment":["movie","film","music","netflix","book","show","award","streaming"]
}

#getting top story ids
def fetch_top_story_ids():
    try:
        url=f"{BASE_URL}/topstories.json"
        res=requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.json()[:TOTAL_IDS_TO_FETCH]
    except:
        return[]

# fetching each story
def fetch_story(story_id):
    try:
        url=f"{BASE_URL}/item/{story_id}.json"
        res=requests.get(url, headers=HEADERS, timeout=5)
        if res.status_code!=200:
            return None
        return res.json()
    except:
        return None

#checking title and assigning category
def classify_story(title):
    if not title:
        return None

    title=title.lower()

    for category, keywords in CATEGORIES.items():
        if any(k in title for k in keywords):
            return category

    return None


# -------- main part -------- #

def main():

    story_ids=fetch_top_story_ids()

    categorized_data={cat: [] for cat in CATEGORIES}
    collected_data=[]

    for idx, story_id in enumerate(story_ids):

        story=fetch_story(story_id)
        if not story:
            continue

        #ignoring non-story items
        if story.get("type")!="story":
            continue

        title=story.get("title")
        if not title:
            continue

        category=classify_story(title)

        #skipping if no category match
        if not category:
            continue

        #skipping if category already filled
        if len(categorized_data[category])>=MAX_PER_CATEGORY:
            continue

        data={
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score",0),
            "num_comments": story.get("descendants",0),
            "author": story.get("by","unknown"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        categorized_data[category].append(data)
        collected_data.append(data)

        print("added:",category)

        #stop when all categories are full
        if all(len(categorized_data[c])>=MAX_PER_CATEGORY for c in CATEGORIES):
            break

        #small progress update
        if (idx+1)%20==0:
            print("processed",idx + 1,"stories...")

        #small delay
        if (idx+1)%50==0:
            time.sleep(1)

    print("\nfilling remaining with dummy data...\n")

    #filling remaining slots with dummy
    for category in CATEGORIES:
        while len(categorized_data[category])<MAX_PER_CATEGORY:
            i=len(categorized_data[category])

            dummy={
                "post_id":100000+len(collected_data),
                "title":f"Dummy title {i+1}",
                "category":category,
                "score":None,
                "num_comments":None,
                "author":"unknown",
                "collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            categorized_data[category].append(dummy)
            collected_data.append(dummy)

    #saving file
    os.makedirs("data",exist_ok=True)

    filename=f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename,"w",encoding="utf-8") as f:
        json.dump(collected_data,f,indent=4)

    print("\ndone. total collected:",len(collected_data))
    print("file saved at:",filename)


if __name__=="__main__":
    main()