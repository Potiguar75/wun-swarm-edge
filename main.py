import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="WUN Swarm Public Edge", description="Global Affiliate Arbitrage Hub"
)

HETZNER_MASTER_URL = "http://204.168.219.251:8000/api/links"


@app.get("/", response_class=HTMLResponse)
async def public_index():
  try:
    async with httpx.AsyncClient() as client:
      response = await client.get(HETZNER_MASTER_URL, timeout=10.0)
      data = response.json()

    links = data.get("data", [])
    total = len(links)

    # Regole CSS corrette con doppie graffe per evitare conflitti
    html_content = f"""
        <html>
            <head>
                <title>WUN Swarm - Micro Business Hub</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }}
                    h1 {{ color: #38bdf8; }}
                    .card {{ background: #1e293b; padding: 15px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #334155; }}
                    a {{ color: #38bdf8; text-decoration: none; font-weight: bold; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <h1>WUN Swarm - Live Micro-Intent Hub</h1>
                <p>Totale opportunità attive: <strong>{total}</strong></p>
        """

    for item in links[:50]:
      intent = item.get("intent", "Offerta")
      url = item.get("monetized_url", "#")
      html_content += f"""
                <div class="card">
                    <p>Intent: <strong>{intent}</strong></p>
                    <a href="{url}" target="_blank">Accedi all'offerta monetizzata &rarr;</a>
                </div>
            """

    html_content += """
            </body>
        </html>
        """
    return html_content

  except Exception as e:
    return f"<h1>Sincronizzazione in corso...</h1><p>Connessione al motore centrale Hetzner in corso. Dettaglio: {e}</p>"