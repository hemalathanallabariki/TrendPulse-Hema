import requests
import time
import json
import os
from datetime import datetime

#================= CONFIG =================
BASE_URL="https://hacker-news.firebaseio.com/v0"
HEADERS={"User-Agent": "TrendPulse/1.0"}

TOTAL_IDS_TO_FETCH=500
MAX_PER_CATEGORY=25

CATEGORIES={
    "technology":["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews":["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science":["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment":["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

#=============== FUNCTIONS ===============

def fetch_top_story_ids():
    try:
        url=f"{BASE_URL}/topstories.json"
        res=requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.json()[:TOTAL_IDS_TO_FETCH]
    except Exception as e:
        print("Error fetching top stories:", e)
        return []


def fetch_story(story_id):
    try:
        url=f"{BASE_URL}/item/{story_id}.json"
        response=requests.get(url, headers=HEADERS, timeout=5)
        
        
        #skip invalid responses
        if response.status_code!=200:
            print(f"HTTP error for {story_id}")
            return None

        data=response.json()
        
        #deleted/unavailable story
        if data is None:
            print(f"Story {story_id} is deleted or unavailable")
            return None

        return data
    #network failure
    except requests.exceptions.RequestException as e:
        print(f"Network error for {story_id}: {e}")
        return None


def classify_story(title):
    if not title:
        return "other"

    title=title.lower()
    #match keywords to category
    for category, keywords in CATEGORIES.items():
        if any(keyword in title for keyword in keywords):
            return category

    return "other"

def fetch_with_retry(story_id, retries=3):
     #retry failed requests
    for _ in range(retries):
        story=fetch_story(story_id)
        if story:
            return story
        time.sleep(0.5)
    return None
#=============== MAIN LOGIC ===============

def main():
    TARGET_TOTAL=125
    story_ids=fetch_top_story_ids()

    collected_data=[]
    category_counts={cat: 0 for cat in CATEGORIES}

    for idx,story_id in enumerate(story_ids):
        story=fetch_with_retry(story_id)
        if not story:
            continue

        title=story.get("title", "")
        category=classify_story(title)

        #Limit only main categories
        if category!="other" and category_counts[category]>=MAX_PER_CATEGORY:
            continue

        data={
            "post_id":story.get("id"),
            "title":title,
            "category":category,
            "score":story.get("score", 0),
            "num_comments":story.get("descendants", 0),
            "author":story.get("by", "unknown"),
            "collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(data)

        if category in category_counts:
            category_counts[category]+=1

        #stop once enough data collected
        if len(collected_data)>=TARGET_TOTAL:
            break

        #Sleep
        if(idx + 1)%25==0:
            print("Sleeping for 2 seconds...")
            time.sleep(2)

    #save output
    os.makedirs("data",exist_ok=True)
    filename=f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename,"w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")


#=============== RUN ===============
if __name__=="__main__":
    main()