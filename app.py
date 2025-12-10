from flask import Flask
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

@app.route("/")
def resumen():
    # Calcular semana pasada
    hoy = datetime.utcnow()
    inicio = hoy - timedelta(days=7)
    fecha_inicio = inicio.strftime("%Y-%m-%d")

    # Obtener la API Key desde variable de entorno
    api_key = os.environ.get("NEWSAPI_KEY")

    # --- CAMBIO APLICADO: Filtro por idioma español (es) y país Argentina (ar) ---
    url = f"https://newsapi.org/v2/everything?q=politica+economia&from={fecha_inicio}&sortBy=publishedAt&apiKey={api_key}&language=es&country=ar"
    
    resp = requests.get(url).json()

    # --- CAMBIO APLICADO: Deduplicación y manejo de enlaces ---
    titulos_unicos = set()
    articulos_filtrados = []

    for art in resp.get("articles", []):
        title = art.get("title")
        # Verificar si el título ya existe en nuestro set de títulos únicos
        if title and title not in titulos_unicos:
            titulos_unicos.add(title)
            # Almacenamos el título Y la URL del artículo
            articulos_filtrados.append({"title": title, "url": art.get("url")})
        
        # Limitar a 10 resultados únicos
        if len(articulos_filtrados) >= 10:
            break

    # --- CAMBIO APLICADO: Renderizado HTML con enlaces <a> ---
    html = "<h1>Resumen semanal de política y economía (Argentina)</h1><ul>"
    for art in articulos_filtrados:
        # Usamos f-string para crear un enlace HTML que el usuario puede clickear
        html += f"<li><a href='{art['url']}' target='_blank'>{art['title']}</a></li>"
    html += "</ul>"
    
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)