"""
Open Movies addon for Stremio-compatible apps such as WuPlay.

This starter catalog lists openly licensed Blender Foundation films.
The films remain hosted by Wikimedia Commons; this addon does not re-host them.
Check each film's attribution/license before redistributing or modifying content.
"""
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Wikimedia Commons file redirects are used for the playable media.
# Playback depends on WuPlay's player accepting the redirected WebM stream.
MOVIES = [
    {
        "id": "openmovie:big-buck-bunny",
        "name": "Big Buck Bunny",
        "year": "2008",
        "description": (
            "A short animated open movie from the Blender Foundation. "
            "License: Creative Commons Attribution 3.0. Credit: Blender Foundation / "
            "www.bigbuckbunny.org. Keep the original credits when showing the complete film."
        ),
        "stream_url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Big_Buck_Bunny_4K.webm",
        "source_url": "https://peach.blender.org/about/",
        "poster": None,
    },
    {
        "id": "openmovie:sintel",
        "name": "Sintel",
        "year": "2010",
        "description": (
            "Fantasy animated short film from the Blender Foundation. "
            "License: Creative Commons Attribution 3.0. Credit: Blender Foundation / sintel.org."
        ),
        "stream_url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Sintel_movie_4K.webm",
        "source_url": "https://durian.blender.org/",
        "poster": None,
    },
    {
        "id": "openmovie:tears-of-steel",
        "name": "Tears of Steel",
        "year": "2012",
        "description": (
            "Science-fiction open movie from the Blender Foundation. "
            "License: Creative Commons Attribution 3.0. Credit: Blender Foundation / mango.blender.org. "
            "Keep the original credits when showing the complete film."
        ),
        "stream_url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Tears_of_Steel_1080p.webm",
        "source_url": "https://mango.blender.org/about/",
        "poster": None,
    },
    {
        "id": "openmovie:elephants-dream",
        "name": "Elephants Dream",
        "year": "2006",
        "description": (
            "An early open movie created by the Blender Foundation and Netherlands Media Art Institute. "
            "Check the original project page for exact attribution and license details."
        ),
        "stream_url": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Elephants_Dream_(2006)_1080p24.webm",
        "source_url": "https://orange.blender.org/",
        "poster": None,
    },
]

MANIFEST = {
    "id": "community.openmovies.wuplay",
    "version": "1.0.0",
    "name": "Open Movies",
    "description": "A small catalog of openly licensed animated and science-fiction short films.",
    "resources": ["catalog", "meta", "stream"],
    "types": ["movie"],
    "idPrefixes": ["openmovie:"],
    "catalogs": [
        {"type": "movie", "id": "open-movies", "name": "Open Movies"},
    ],
}

MOVIE_BY_ID = {movie["id"]: movie for movie in MOVIES}


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


def to_meta(movie):
    meta = {
        "id": movie["id"],
        "type": "movie",
        "name": movie["name"],
        "description": movie["description"],
        "releaseInfo": movie["year"],
        "links": [{"name": "Official project / license information", "url": movie["source_url"]}],
    }
    if movie.get("poster"):
        meta["poster"] = movie["poster"]
        meta["background"] = movie["poster"]
    return meta


@app.route("/")
def home():
    return (
        "Open Movies addon is running. Open /manifest.json to install it. "
        "Playback must be tested in your WuPlay version."
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "catalog_items": len(MOVIES)})


@app.route("/manifest.json")
def manifest():
    return jsonify(MANIFEST)


@app.route("/catalog/<type_>/<cat_id>.json")
@app.route("/catalog/<type_>/<cat_id>/<extra>.json")
def catalog(type_, cat_id, extra=None):
    if type_ != "movie" or cat_id != "open-movies":
        return jsonify({"metas": []})
    return jsonify({"metas": [to_meta(movie) for movie in MOVIES]})


@app.route("/meta/<type_>/<path:item_id>.json")
def meta(type_, item_id):
    if type_ != "movie":
        return jsonify({"meta": {}})
    movie = MOVIE_BY_ID.get(item_id)
    return jsonify({"meta": to_meta(movie) if movie else {}})


@app.route("/stream/<type_>/<path:item_id>.json")
def stream(type_, item_id):
    if type_ != "movie":
        return jsonify({"streams": []})
    movie = MOVIE_BY_ID.get(item_id)
    if not movie:
        return jsonify({"streams": []})
    return jsonify({
        "streams": [
            {
                "name": "Open Movies (Wikimedia Commons)",
                "title": "Play open-licensed film (WebM; compatibility may vary)",
                "url": movie["stream_url"],
            },
            {
                "name": "Official project page",
                "title": "Open source / license page",
                "externalUrl": movie["source_url"],
            },
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7000)))
