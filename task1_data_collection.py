import re
import requests
import time
import os
import json
from datetime import datetime

#base URLs
TOP_STORIES_URL="https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL="https://hacker-news.firebaseio.com/v0/item/{}.json"

#request headers
HEADERS={"User-Agent":"TrendPulse/1.0"}


#categories and keywords
CATEGORIES={
    "technology":["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews":["war","government","country","president","election","climate","attack","global"],
    "sports":["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science":["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment":["movie","film","music","netflix","game","book","show","award","streaming"]
}

#function to fetch JSON data from a URL
def fetch_json(url):
    try:
        response=requests.get(url,headers=HEADERS,timeout=10)
        if response.status_code==200:
            return response.json()
        else:
            print(f"Failed request: {url}")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


#function to check category match
def get_category(title):
    title = title.lower()

    #extract words only (avoids 'ai' in 'said')
    words=re.findall(r'\b\w+\b',title)

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in words:
                return category

    return None  


#function to create dummy story
def create_dummy(category, index):
    return {
        "post_id": f"dummy_{category}_{index}",
        "title": f"Dummy {category} story {index}",
        "category": category,
        "score": None,
        "num_comments": None,
        "author": "system",
        "collected_at": datetime.now().isoformat()
    }


def main():
    #fetch top story IDs
    print("Fetching top stories...")
    top_ids=fetch_json(TOP_STORIES_URL)
    
    if not top_ids:
        print("Failed to fetch top stories. Exiting.")
        return
    #limit to first 500
    top_ids=top_ids[:500]  

    all_stories=[]

    #process one category at a time
    for category,keywords in CATEGORIES.items():
        print(f"\nProcessing category: {category}")

        category_stories=[]
        #fetch stories until we have 25 for this category
        for story_id in top_ids:
            if len(category_stories)>=25:
                break
            #fetch story details
            story=fetch_json(ITEM_URL.format(story_id))
            if not story:
                continue
            print(f"fetching story {story_id}...")
            title=story.get("title","")
            if not title:
                continue

            #check if story matches category
            if get_category(title)==category:
                story_data={
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score",0),
                    "num_comments": story.get("descendants",0),
                    "author": story.get("by","unknown"),
                    "collected_at": datetime.now().isoformat()
                }
                
                category_stories.append(story_data)
            
        print(f"Found {len(category_stories)} stories for {category}")

        #filling the remaining with dummy data
        print("Filling category with dummy data ")
        if len(category_stories)<25:
            print(f"Filling {category} with dummy data...")
            for i in range(len(category_stories),25):
                category_stories.append(create_dummy(category,i))

        print(f"Collected {len(category_stories)} stories for {category}")

        #add to main list
        all_stories.extend(category_stories)

        #sleep after each category
        print("Sleeping for 2 seconds...\n")
        time.sleep(2)

    #save to JSON
    if not os.path.exists("data"):
        os.makedirs("data")

    filename=f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
    #save the collected stories to a JSON file
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(all_stories,f,indent=4)

    print(f"\nCollected {len(all_stories)} stories.")
    print(f"Saved to {filename}")


if __name__=="__main__":
    main()