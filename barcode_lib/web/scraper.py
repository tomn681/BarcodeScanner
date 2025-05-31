import json
from typing import List
from pathlib import Path
from urllib.parse import quote_plus, urlparse
from googlesearch import search
import requests
from bs4 import BeautifulSoup

CONFIG_PATH = Path(__file__).parent / "webconfig.json"

def get_priority_sites():
    return json.loads(CONFIG_PATH.read_text())["priority"]

def google_search(sku: str, domains: List[str]) -> str:
    print(f"[Search] Starting search for SKU: {sku}")

    for domain in domains:
        query = f"site:{domain} {sku}"
        print(f"[Search] Trying: {query}")
        results = list(search(query, num_results=1))
        for result in results:
            if result.strip():
                print(f"[Search] Found in priority: {result}")
                return result

    print("[Search] No result in priority sites, falling back to general search...")
    results = list(search(sku, num_results=1))
    for result in results:
        if result.strip():
            print(f"[Search] Found general result: {result}")
            return result

    print("[Search] No result found at all.")
    return None

def scrape_product_info(sku: str) -> dict:
    sites = get_priority_sites()
    url = google_search(sku, sites)
    print(f"[Scraper] URL selected: {url}")

    if not url:
        return {
            "product": "Producto desconocido",
            "brand": "Desconocida",
            "category": "General",
            "image": None
        }

    return scrape_generic(url)

    
def scrape_generic(url: str) -> dict:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/113.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=5)

        # Si aún hay error (ej. 406), mostrar mensaje:
        if resp.status_code != 200:
            return {
                "product": f"Error {resp.status_code} {resp.reason}",
                "brand": "Desconocida",
                "category": "General",
                "image": None
            }

        soup = BeautifulSoup(resp.text, "html.parser")


        # Nombre del producto
        name_tag = soup.find("h1") or soup.title
        name = name_tag.text.strip() if name_tag else "Producto desconocido"

        # Imagen
        image = None
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if any(kw in src.lower() for kw in ["product", "main", "item"]) and src.endswith((".jpg", ".png", ".jpeg")):
                image = src
                break

        return {
            "product": name,
            "brand": "Desconocida",
            "category": "General",
            "image": image
        }

    except Exception as e:
        print(f"[Scraper] Error scraping: {e}")
        return {
            "product": "Producto desconocido",
            "brand": "Desconocida",
            "category": "General",
            "image": None
        }
