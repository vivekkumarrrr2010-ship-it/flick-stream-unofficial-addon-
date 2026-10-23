# Open Movies WuPlay / Stremio-compatible addon

This is a starter addon that lists a few openly licensed Blender Foundation films.
It does not host or re-upload the media; playback links point to Wikimedia Commons file redirects.

## Files
- `app.py` — Flask addon service
- `requirements.txt` — Python dependencies

## Run locally
```bash
python -m pip install -r requirements.txt
python app.py
```
Then check:
- `http://127.0.0.1:7000/health`
- `http://127.0.0.1:7000/manifest.json`
- `http://127.0.0.1:7000/catalog/movie/open-movies.json`

## Deploy to Render
Create a Web Service connected to the repository containing these files:
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Free plan may sleep when idle.

After deployment, add `https://YOUR-SERVICE.onrender.com/manifest.json` in WuPlay.

## Important limitations
- This is a starter catalog, not a commercial movie library and not a FlickyStream integration.
- The catalog currently has movies/short films only, not episodic series.
- WuPlay must support the stream object and the WebM format, and Wikimedia's redirects must work from your device. Test actual playback.
- Posters are omitted until reliable, licensed poster image URLs are verified.
- Keep attribution/license information with each film. Confirm current terms before any public or commercial distribution.
