import os
import sys
from datetime import datetime, UTC
from pathlib import Path

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# =========================================================================== #
# basic config / auth
# =========================================================================== #
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
if not CLIENT_ID or not CLIENT_SECRET:
    sys.exit("Missing SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET in .env")

SCOPE = (
    "playlist-read-private "
    "playlist-read-collaborative "
    "playlist-modify-public "
    "playlist-modify-private"
)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=Path.home() / ".cache_spotify_token",
        open_browser=True,
    )
)

user = sp.current_user()
USER_ID = user["id"]
print(f"Logged in as {user['display_name']} ({USER_ID})\n")

# =========================================================================== #
# helpers
# =========================================================================== #

def iter_playlists(batch_size: int = 50):
    offset = 0
    while True:
        page = sp.current_user_playlists(limit=batch_size, offset=offset)
        items = page.get("items", [])
        if not items:
            break
        yield from items
        offset += batch_size

# =========================================================================== #
# make playlists private
# =========================================================================== #

def make_playlists_private():
    updated = already_private = skipped = 0
    for pl in iter_playlists():
        if pl["owner"]["id"] != USER_ID:
            skipped += 1
            continue
        if not pl["public"]:
            already_private += 1
            continue
        sp.playlist_change_details(pl["id"], public=False)
        updated += 1
        print(f"Made private: {pl['name']}")
    print("\nDone")
    print(f"  Updated : {updated}")
    print(f"  Already : {already_private}")
    print(f"  Skipped : {skipped}")

# =========================================================================== #
# unfollow non‑owned playlists
# =========================================================================== #

def unfollow_non_owned():
    stamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    report_path = Path(f"unfollowed_playlists_{stamp}.txt")
    unfollowed = kept = 0
    with report_path.open("w", encoding="utf-8") as fh:
        for pl in iter_playlists():
            if pl["owner"]["id"] == USER_ID:
                kept += 1
                continue
            fh.write(f"{pl['name']} | {pl['external_urls']['spotify']}\n")
            sp.current_user_unfollow_playlist(pl["id"])
            unfollowed += 1
            print(f"Unfollowed: {pl['name']}")
    print("\nDone")
    print(f"  Unfollowed : {unfollowed}")
    print(f"  Kept       : {kept}")
    print(f"  Report     : {report_path.resolve()}")

# =========================================================================== #
# main
# =========================================================================== #

def main():
    menu = (
        "Choose an option:\n"
        "  1) Make every playlist you own private\n"
        "  2) Unfollow playlists you don't own\n"
        "  q) Quit\n\n"
        "Enter choice (1/2/q): "
    )
    choice = input(menu).strip().lower()
    if choice == "1":
        make_playlists_private()
    elif choice == "2":
        unfollow_non_owned()
    else:
        print("Nothing to do – exiting.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")

