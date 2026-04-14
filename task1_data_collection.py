import requests
import time
import json
import os
from datetime import datetime

#----------- CONFIG ----------- #
#base api url
BASE="https://hacker-news.firebaseio.com/v0"
HEADERS={"User-Agent":"TrendPulse/1.0"}

#limits for how much data we want
LIMIT_PER_CAT=25
MAX_FETCH=500

#keywords for each category
CATEGORY_MAP={
    "technology":["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "entertainment":["movie","film","music","netflix","game","book","show","award","streaming"],
    "worldnews":["war","government","country","president","election","climate","attack","global"],
    "science":["research","study","space","physics","biology","discovery","nasa","genome"],
    "sports":["nfl","nba","fifa","sport","game","team","player","league","championship"]
}


# ----------- FETCHING ----------- #
#get top story ids from hackernews
def get_top_ids():
    try:
        res=requests.get(f"{BASE}/topstories.json",eaders=HEADERS)
        res.raise_for_status()
        return res.json()[:MAX_FETCH]
    except Exception as err:
        print(f"Top stories fetch failed:{err}")
        return []


#get details of one story
def get_story_data(sid):
    try:
        res=requests.get(f"{BASE}/item/{sid}.json",headers=HEADERS)
        res.raise_for_status()
        return res.json()
    except Exception:
        print(f"Story fetch failed:{sid}")
        return None


# ----------- CLASSIFICATION ----------- #
#checking which category the title belongs to
def detect_category(text):
    if not text:
        return None

    t=text.lower()

    #match keywords with title
    for cat in CATEGORY_MAP:
        if any(word in t for word in CATEGORY_MAP[cat]):
            return cat

    return None

#----------- DATA PROCESSING ----------- #

#building final record for json
def build_record(story,category):
    return {
        "post_id":story.get("id"),
        "title":story.get("title", ""),
        "category":category,
        "score":story.get("score", 0),
        "num_comments":story.get("descendants", 0),
        "author":story.get("by","unknown"),
        "collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


#creating dummy data if category is not full
def generate_dummy(category,index):
    return {
        "post_id":10000+index,
        "title":f"Dummy Title{index+1}for{category}",
        "category":category,
        "score":None,
        "num_comments":None,
        "author":"unknown",
        "collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


#----------- MAIN PIPELINE ----------- #

def run_pipeline():
    ids = get_top_ids()

    #storing data category-wise
    categorized={k:[] for k in CATEGORY_MAP}
    all_data=[]

    #processing one category at a time
    for cat in CATEGORY_MAP.keys():
        print(f"\nProcessing category:{cat}")

        count=0
        idx=0

        #going through story ids until we fill this category
        while idx<len(ids) and count<LIMIT_PER_CAT:
            sid=ids[idx]
            idx+=1

            print(f"Fetching story {sid}")
            story=get_story_data(sid)

            if not story:
                continue

            title=story.get("title", "")
            assigned=detect_category(title)

            #add only if category matches
            if assigned==cat:
                record=build_record(story,cat)
                categorized[cat].append(record)
                all_data.append(record)
                count+=1

        #if not enough real data, fill with dummy
        while len(categorized[cat])<LIMIT_PER_CAT:
            dummy=generate_dummy(cat,len(categorized[cat]))
            categorized[cat].append(dummy)
            all_data.append(dummy)

        print(f"Completed category '{cat}' with {len(categorized[cat])} stories.")
        print("Sleeping for 2 seconds")
        time.sleep(2)

    return all_data


#----------- SAVE OUTPUT ----------- #

def save_output(data):
    #make sure data folder exists
    os.makedirs("data",exist_ok=True)

    fname=f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    #save json file
    with open(fname,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)

    print(f"\nCollected {len(data)} stories. aved to {fname}")


#----------- EXECUTION ----------- #

if __name__=="__main__":
    result=run_pipeline()
    save_output(result)