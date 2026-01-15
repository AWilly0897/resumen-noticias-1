from flask import Flask, url_for
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

def menu():
    return """
    <nav style="background-color:#eee;padding:10px;">
        <a href="/">Resumen</a>
    </nav>
    """

@app.route("/")
def resumen():
    hoy = datetime.utcnow()
    inicio = hoy - timedelta(days=7)
    fecha_inicio = inicio.strftime("%Y-%m-%d")

    api_key = os.environ.get("NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/everything?q=politica+economia&from={fecha_inicio}&sortBy=publishedAt&apiKey={api_key}"
    resp = requests.get(url).json()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Resumen semanal</title>
        <link rel="icon" href="{url_for('static', filename='Favicon.ico')}" type="image/x-icon" />
    </head>
    <body>
        {menu()}
        <h1>Resumen semanal de política y economía</h1>
        <ul>
    """
    for art in resp.get("articles", [])[:10]:
        html += f"<li>{art['publishedAt']} - {art['title']} ({art['source']['name']})</li>"
    html += "</ul></body></html>"
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

