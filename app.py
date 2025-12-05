from flask import Flask
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def resumen():
    # Calcular semana pasada
    hoy = datetime.utcnow()
    inicio = hoy - timedelta(days=7)
    fecha_inicio = inicio.strftime("%Y-%m-%d")

    # Ejemplo con NewsAPI (requiere API key gratuita)
    url = f"https://newsapi.org/v2/everything?q=politica+economia&from={fecha_inicio}&sortBy=publishedAt&apiKey=TU_API_KEY"
    resp = requests.get(url).json()

    # Generar resumen simple
    titulares = [art["title"] for art in resp.get("articles", [])[:10]]

    # Renderizar en HTML básico
    html = "<h1>Resumen semanal de política y economía</h1><ul>"
    for t in titulares:
        html += f"<li>{t}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
