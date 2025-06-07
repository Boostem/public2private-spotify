"""
make_playlists_private.py
Set every playlist you own to private.

Requires:
  pip install spotipy python-dotenv
"""

import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

if not (CLIENT_ID and CLIENT_SECRET):
    sys.exit("Client ID or Client Secret missing in .env")

SCOPE = (
    "playlist-read-private "
    "playlist-modify-public "
    "playlist-modify-private"
)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=True,
        cache_path=".spotipy_token"
    )
)

user = sp.current_user()
user_id = user["id"]
print(f"Authenticated as {user['display_name']} ({user_id})")

updated = skipped_private = skipped_not_owner = 0
offset = 0
page_size = 50

while True:
    page = sp.current_user_playlists(limit=page_size, offset=offset)
    items = page["items"]
    if not items:
        break

    for playlist in items:
        if playlist["owner"]["id"] != user_id:
            skipped_not_owner += 1
            continue
        if not playlist["public"]:
            skipped_private += 1
            continue

        sp.playlist_change_details(playlist_id=playlist["id"], public=False)
        updated += 1
        print(f"Made private: {playlist['name']}")

    offset += page_size

print("\nSummary")
print(f"  Updated playlists : {updated}")
print(f"  Already private   : {skipped_private}")
print(f"  Not owned         : {skipped_not_owner}")

