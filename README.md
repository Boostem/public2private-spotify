# public2private-spotify

A simple script that loops through your Spotify playlists and makes them private. Useful if you’ve accidentally made a bunch of playlists public over the years and want to lock things down.

## Getting Started

1. Clone the repo

   git clone git@github.com:Boostem/public2private-spotify.git

   cd public2private-spotify

3. Set up a virtual environment

   python3 -m venv .venv

   source .venv/bin/activate  # or .venv\Scripts\activate on Windows

5. Install dependencies

   pip install -r requirements.txt

## Setting up your Spotify app

This script uses the Spotify Web API, so you need your own app to authenticate.

1. Go to https://developer.spotify.com/dashboard
2. Log in and click “Create an App”
3. Give it a name and description (anything is fine)
4. Under the app settings, add this redirect URI:

   http://127.0.0.1:8888/callback

5. Save your changes

## Creating your .env file

Create a file called `.env` in the root of the project and add this:

   SPOTIPY_CLIENT_ID=your_spotify_client_id
   
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback

You can copy `.env-example` as a starting point if needed.

## Running the script

Once you’ve got everything set up:

   python private_spotify.py

It’ll open a browser window, ask you to log in to Spotify and approve access. Then it will loop through your playlists and set each one to private (if it’s owned by you and isn’t already private).

## Notes

- It only touches playlists you own.
- If a playlist is already private, it skips it.
- Playlists you’ve followed but don’t own are ignored.
