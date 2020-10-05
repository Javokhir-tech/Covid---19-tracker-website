import os
import requests
import urllib.parse
import json
from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(country):
    """ Look up for country affected by covid - 19 """
    
    #url = "https://www.trackcorona.live/api/countries"
    url = "https://api.covid19api.com/summary"
    payload = {}
    #headers= {}
    headers= {'X-Access-Token':'5cf9dfd5-3449-485e-b5ae-70a60e997864'}
    
    response = requests.request("GET", url, headers=headers, data = payload)
    
    try:
        info = response.json()    
        return {
            "Country": info['Countries'],
            "Global": info["Global"]
        }
    except (KeyError, TypeError, ValueError):
        return None