import os
import json
import tweepy
import requests
from datetime import datetime, timezone

# --- Konfiguration ---
# Dein Twitter Bearer Token. Dies sollte als GitHub Secret gespeichert werden!
# Beispiel: TWITTER_BEARER_TOKEN
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Der Twitter-Handle, dessen Tweets du abrufen möchtest (ohne '@')
TWITTER_USERNAME = "mschultheiss83" # Passe dies an deinen Twitter-Handle an

# Pfad zur JSON-Datei, in der die Tweets gespeichert werden
DATA_FILE_PATH = "_data/tweets.json"

# Anzahl der Tweets, die pro API-Anfrage abgerufen werden sollen (max. 100 für get_users_tweets)
MAX_RESULTS_PER_REQUEST = 100

# --- Funktionen ---

def get_twitter_client():
    """Initialisiert und gibt einen Tweepy Client für die Twitter API v2 zurück."""
    if not BEARER_TOKEN:
        raise ValueError("TWITTER_BEARER_TOKEN Umgebungsvariable ist nicht gesetzt.")
    return tweepy.Client(BEARER_TOKEN) [1, 2]

def fetch_user_tweets(client, username, max_results=MAX_RESULTS_PER_REQUEST):
    """
    Ruft die neuesten Tweets eines Benutzers ab, inklusive öffentlicher Metriken.
    Verwendet Paginierung, um mehr als 100 Tweets abzurufen, falls nötig.
    """
    user_id = client.get_user(username=username).data.id
    all_tweets =
    pagination_token = None

    while True:
        response = client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            tweet_fields=["created_at", "public_metrics"],
            pagination_token=pagination_token
        ) [3, 4]

        if response.data:
            all_tweets.extend(response.data)

        # Überprüfe, ob es eine nächste Seite gibt
        if 'next_token' in response.meta:
            pagination_token = response.meta['next_token']
        else:
            break # Keine weiteren Seiten

    return all_tweets

def get_oembed_html(tweet_id, author_username):
    """
    Ruft das einbettbare HTML für einen Tweet über die oEmbed API ab.
    Verwendet omit_script=true, um redundantes Laden von widgets.js zu vermeiden.
    """
    oembed_url = f"https://publish.twitter.com/oembed?url=https://twitter.com/{author_username}/status/{tweet_id}&omit_script=true" [5, 6]
    try:
        response = requests.get(oembed_url)
        response.raise_for_status() # Löst einen HTTPError für schlechte Antworten (4xx oder 5xx) aus
        return response.json().get("html")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen von oEmbed HTML für Tweet {tweet_id}: {e}")
        return None

def load_existing_tweets(file_path):
    """Lädt vorhandene Tweets aus der JSON-Datei."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warnung: {file_path} ist keine gültige JSON-Datei. Starte mit leerer Liste.")
                return
    return[7]

def save_tweets(file_path, tweets_data):
    """Speichert die verarbeiteten Tweets in der JSON-Datei."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(tweets_data, f, indent=2, ensure_ascii=False) [7]
    print(f"Tweets erfolgreich in {file_path} gespeichert.")

def main():
    print("Starte Tweet-Abruf...")

    client = get_twitter_client()

    # Lade vorhandene Tweets, um Metadaten zu erhalten
    existing_tweets = load_existing_tweets(DATA_FILE_PATH)
    existing_tweets_map = {tweet['id']: tweet for tweet in existing_tweets}

    # Rufe die neuesten Tweets ab
    fetched_tweets = fetch_user_tweets(client, TWITTER_USERNAME)
    print(f"Abgerufene Tweets von @{TWITTER_USERNAME}: {len(fetched_tweets)}")

    processed_tweets =
    for tweet in fetched_tweets:
        tweet_id = str(tweet.id)

        # Versuche, oEmbed HTML abzurufen
        html_embed_code = get_oembed_html(tweet_id, TWITTER_USERNAME)
        if not html_embed_code:
            print(f"Überspringe Tweet {tweet_id} aufgrund fehlendem oEmbed HTML.")
            continue

        # Bereite die Daten für die JSON-Datei vor
        processed_tweet = {
            "id": tweet_id,
            "text": tweet.text,
            "author_username": TWITTER_USERNAME,
            "created_at": tweet.created_at.isoformat(),
            "public_metrics": tweet.public_metrics,
            "html_embed_code": html_embed_code,
            "original_url": f"https://twitter.com/{TWITTER_USERNAME}/status/{tweet_id}"
        }

        # Behalte manuell hinzugefügte Metadaten bei, falls der Tweet bereits existiert
        if tweet_id in existing_tweets_map:
            old_tweet = existing_tweets_map[tweet_id]
            # Beispiel: Wenn du manuell 'is_top_post' oder 'category' hinzufügst
            if 'is_top_post' in old_tweet:
                processed_tweet['is_top_post'] = old_tweet['is_top_post']
            if 'category' in old_tweet:
                processed_tweet['category'] = old_tweet['category']

        processed_tweets.append(processed_tweet)

    # Sortiere die Tweets nach Erstellungsdatum (neueste zuerst)
    processed_tweets.sort(key=lambda x: x['created_at'], reverse=True)

    # Speichere die aktualisierten Tweets
    save_tweets(DATA_FILE_PATH, processed_tweets)
    print("Tweet-Abruf und Speicherung abgeschlossen.")

if __name__ == "__main__":
    main()