import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re
from datetime import datetime
import os
from agents import USER_AGENTS
import urllib.parse
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
TOKEN_API = os.getenv("TOKEN_API")

def get_headers():
    """Retorna headers com User-Agent aleatório e cookies/referer"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
        "DNT": "1",
    }

def fazer_requisicao(url, max_tentativas=3):
    """Faz uma requisição HTTP com até 3 tentativas e User-Agent aleatório."""
    for tentativa in range(1, max_tentativas + 1):
        try:
            token = TOKEN_API
            if not token:
                print("TOKEN_API não encontrado em .env; verifique o arquivo casasbahia/.env")
                return None
            encoded_url = urllib.parse.quote(url)
            geoCode="br"
            
            url_scrapped = f"http://api.scrape.do/?token={token}&url={url}&geoCode={geoCode}"
            
            print(f"Tentativa {tentativa} para {url_scrapped}")
            response = requests.get(url_scrapped, timeout=15)
            
            print(f"Status Code: {response.status_code}")
            
            response.raise_for_status()

            return response
        except Exception as e:
            print(f"Erro na tentativa {tentativa}: {e}")
            if tentativa < max_tentativas:
                espera = random.uniform(3, tentativa * 5)

                print(f"Aguardando {espera:.1f}s antes da próxima tentativa...")
                time.sleep(espera)
            else:
                print("Falha após 3 tentativas.")
    return None


def coletar_opinioes(produto):
    """Acessa o link do produto e coleta suas opiniões."""
    url = produto["link"]
    print(f"\nColetando opiniões de: {produto['titulo']}")
    comentarios = []

    response = fazer_requisicao(url)
    if not response:
        return comentarios

    soup = BeautifulSoup(response.text, "html.parser")

    konfidency_div = soup.find("div", class_="konfidency-reviews-summary")
    id_avaliacoes = konfidency_div["data-sku"] if konfidency_div and konfidency_div.has_attr("data-sku") else "N/A"
    try:
        comentarios.append({
            "categoria": produto.get("categoria", "N/A"),
            "pesquisa": produto.get("pesquisa", "N/A"),
            "titulo": produto.get("titulo", "N/A"),
            "id_produto": produto.get("id_produto", "N/A"),
            "id_avaliacoes": id_avaliacoes,
        })
    except Exception as e:
        print(f"Erro ao processar comentário: {e}")
        # continue

    return comentarios

def main():
    entrada_csv = os.path.join(project_root, 'data', 'raw', 'produtos_casasbahia.csv')
    saida_csv = os.path.join(project_root, 'data', 'raw', 'avaliacoes_casasbahia.csv')

    if not os.path.exists(entrada_csv):
        print(f"Arquivo '{entrada_csv}' não encontrado.")
        return

    arquivo_existe = os.path.exists(saida_csv)

    with open(saida_csv, "a", newline="", encoding="utf-8") as csv_saida, \
         open(entrada_csv, "r", encoding="utf-8") as csv_entrada:

        leitor = csv.DictReader(csv_entrada, delimiter='|')
        campos = [
            "categoria",
            "pesquisa",
            "titulo",
            "id_produto",
            "id_avaliacoes",
        ]
        writer = csv.DictWriter(csv_saida, fieldnames=campos, delimiter='|')

        if not arquivo_existe:
            writer.writeheader()

        for produto in leitor:
            if not produto.get("link"):
                continue

            comentarios = coletar_opinioes(produto)
            for linha in comentarios:
                writer.writerow(linha)
            time.sleep(random.uniform(5, 8))

    print(f"\nColeta concluída! Dados adicionados em '{saida_csv}'.")


if __name__ == "__main__":
    main()