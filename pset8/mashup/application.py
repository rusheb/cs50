import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    return render_template("index.html")


@app.route("/articles")
def articles():
    """Look up articles for geo"""
    postcode = request.args.get('geo')
    if not postcode:
        raise RuntimeError('could not obtain location')

    return jsonify(lookup(request.args.get('geo')))


@app.route("/search")
def search():
    raw_query = request.args.get('q')
    if not raw_query:
        raise RuntimeError('no query')

    query = (raw_query
             .replace("%20", " ")
             .replace("+", " ")
             .replace(",", " ")
             .split(" "))

    print(query)

    previous = []
    for i in range(len(query)):
        word = query[i]
        word_ = query[i] + '%'
        _word_ = '%' + query[i] + '%'

        sql = "SELECT * FROM places \
                 WHERE country_code = :q \
                 OR postal_code LIKE :q_ \
                 OR place_name LIKE :_q_ \
                 OR admin_name1 LIKE :_q_ \
                 OR admin_code1 = :q \
                 OR admin_code2 = :q"

        if i == 0:
            result = db.execute(sql, q=word, q_=word_, _q_=_word_)
        else:
            previous = result
            result = db.execute(sql, q=word, q_=word_, _q_=_word_)
            result = [n for n in previous for m in result if n['postal_code'] == m['postal_code']]

    return jsonify(result)


@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
