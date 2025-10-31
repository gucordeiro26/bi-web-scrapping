import csv
import requests
import json
import time
import re
from datetime import datetime
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

input_csv = os.path.join(project_root, 'data', 'raw', 'avaliacoes_casasbahia.csv')
output_csv = os.path.join(project_root, 'data', 'raw', 'comentarios_produtos.csv')

def coletar_dados(id_avaliacoes):
    url = f"https://reviews-api.konfidency.com.br/casasbahia/{id_avaliacoes}/summary/helpfulScore,desc?pageSize=100&page=1"
    print(url)
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao requisitar {id_avaliacoes}: {e}")
        return None


def sanitize_text(text):
    """Remove quebras de linha, colapsa espaços e remove o delimitador '|' para garantir uma linha por comentário no CSV."""
    if text is None:
        return ""
    
    s = re.sub(r"[\r\n]+", " ", str(text))
    
    s = s.replace("|", "")
    
    s = re.sub(r"\s+", " ", s).strip()
    return s

ids = []
with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='|')
    for row in reader:
        if row.get('id_avaliacoes') != 'N/A':
            ids.append(row.get('id_avaliacoes', '').strip())

with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile, delimiter='|')
    writer.writerow([
        "id_produto",
        "id_avaliacoes",
        "id_comentario",
        "rating_do_comentario",
        "quantidade_avaliacoes_do_produto",
        "comentario_about_produto",
        "data_coleta"
    ])

    for id_avaliacoes in ids:
        print(id_avaliacoes)
        data = coletar_dados(id_avaliacoes)

        if not data:
            
            time.sleep(1)
            continue

        for produto in data.get("reviews", []):
            id_produto = produto.get("_id", "")
            qtd_avaliacoes = produto.get("reviewCount", 0)
            comentarios = produto.get("reviews", [])

            for comentario in comentarios:
                id_comentario = comentario.get("_id", "")
                rating = comentario.get("rating", "")
                raw_text = comentario.get("text", "")
                texto = sanitize_text(raw_text)
                data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                writer.writerow([
                    id_produto,
                    id_avaliacoes,
                    id_comentario,
                    rating,
                    qtd_avaliacoes,
                    texto,
                    data_coleta
                ])

            time.sleep(1)