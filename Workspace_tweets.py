import os
import json

# Konfiguration
DATA_FILE = "_data/tweets.json"
CATEGORIES_DIR = "_pages/categories/"

def fetch_tweets():
    # … Dein bestehender Code zum Abrufen der Tweets …
    return tweets  # Liste von Tweet-Dicts

def compute_relevance(tweets):
    for tweet in tweets:
        metrics = tweet.get("public_metrics", {})
        # Gewichtete Relevanz: 70% Likes, 30% Retweets
        tweet["relevance_score"] = (
            metrics.get("like_count", 0) * 0.7 +
            metrics.get("retweet_count", 0) * 0.3
        )
    return tweets

def save_data(tweets):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

def generate_category_pages(tweets):
    os.makedirs(CATEGORIES_DIR, exist_ok=True)
    categories = {t.get("category", "uncategorized") for t in tweets}
    for cat in categories:
        filename = f"{CATEGORIES_DIR}{cat.lower()}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"---\n")
            f.write(f"layout: category\n")
            f.write(f"title: \"Kategorie: {cat.title()}\"\n")
            f.write(f"permalink: /categories/{cat.lower()}/\n")
            f.write(f"---\n")
            f.write("{% assign cat_tweets = site.data.tweets ")
            f.write(f"| where: \"category\", \"{cat}\" %}\n")
            f.write("{% for tweet in cat_tweets %}\n")
            f.write("  {% include tweet.html tweet=tweet %}\n")
            f.write("{% endfor %}\n")

def main():
    tweets = fetch_tweets()
    tweets = compute_relevance(tweets)  # Relevance-Score hinzufügen
    save_data(tweets)
    generate_category_pages(tweets)     # Statische Kategorieseiten

if __name__ == "__main__":
    main()
