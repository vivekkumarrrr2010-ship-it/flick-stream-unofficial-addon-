"""
FlickyStream external-link addon for Stremio-compatible apps such as WuPlay.

This is intentionally a link-only integration:
- It does not scrape FlickyStream.
- It does not extract, proxy, or redistribute video streams.
- It provides one catalog item that opens the website externally.
Actual website catalog integration requires an authorized, documented interface.
"""
import os
from flask import Flask, jsonify

app = Flask(__name__)

SITE_URL = "https://flickystream.mov/"

MANIFEST = {
    "id": "community.flickystream.external-link",
    "version": "1.0.0",
    "name": "FlickyStream Link",
    "description": "External link to the FlickyStream website; no catalog scraping or stream extraction.",
    "resources": ["catalog", "meta", "stream"],
    "types": ["movie"],
    "idPrefixes": ["flickylink:"],
    "catalogs": [
        {"type": "movie", "id": "flicky-home", "name": "FlickyStream Website"}
    ],
}

META = {
    "id": "flickylink:home",
    "type": "movie",
    "name": "Open FlickyStream",
    "description": (
        "Opens the FlickyStream website externally. "
        "This addon does not fetch movie listings or provide video streams."
    ),
    "posterShape": "landscape",
    "links": [{"name": "FlickyStream website", "url": SITE_URL}],
}


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


@app.route("/")
def home():
    return "FlickyStream link addon is running. Open /manifest.json to install it."


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/manifest.json")
def manifest():
    return jsonify(MANIFEST)


@app.route("/catalog/<type_>/<cat_id>.json")
@app.route("/catalog/<type_>/<cat_id>/<extra>.json")
def catalog(type_, cat_id, extra=None):
    if type_ == "movie" and cat_id == "flicky-home":
        return jsonify({"metas": [META]})
    return jsonify({"metas": []})


@app.route("/meta/<type_>/<path:item_id>.json")
def meta(type_, item_id):
    if type_ == "movie" and item_id == "flickylink:home":
        return jsonify({"meta": META})
    return jsonify({"meta": {}})


@app.route("/stream/<type_>/<path:item_id>.json")
def stream(type_, item_id):
    if type_ == "movie" and item_id == "flickylink:home":
        return jsonify({
            "streams": [{
                "name": "External website",
                "title": "Open FlickyStream in browser",
                "externalUrl": SITE_URL
            }]
        })
    return jsonify({"streams": []})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7000)))
