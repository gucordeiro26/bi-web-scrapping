Casas Bahia — Web Scraping (módulo)

Este diretório contém utilitários e agentes para coletar informações de produtos do site Casas Bahia. O objetivo é fornecer scripts reutilizáveis para obter listas de produtos, detalhes e comentários usando uma API de scraping (ex.: scrape.do) ou scraping próprio quando aplicável.

## Principais funcionalidades
- Coletar listas de produtos e metadados (preço, título, código, categoria).
- Obter detalhes de um produto específico (descrição completa, especificações, imagens).
- Agentes organizados em `agents.py` e scripts utilitários para chamadas/sincronização.

## Estrutura dos arquivos
- `agents.py` — classes/funções que encapsulam lógica de requisição e parsing.
- `getProduct.py` — script para coletar / listar produtos (uso direto ou via agendamento).
- `getDetails.py` — script para coletar detalhes de produtos a partir de uma lista/identificador.
- `.env` — arquivo de configuração com chaves/sensíveis (não comitar chaves reais ao VCS).

## Requisitos
- Python 3.8+ (recomendado)
- Dependências listadas no `requirements.txt` na raiz do projeto.

```
SCRAPEDO_API_KEY=your_api_key_here
```

## Como usar (rápido)
1. Crie e ative um ambiente virtual (exemplo para shell bash):

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

2. Configure a chave no `.env` (ou export diretamente):

```bash
export SCRAPEDO_API_KEY="sua_chave_aqui"
```

3. Executar os scripts (exemplos):

```bash
# coletar lista de produtos (ajuste args dentro do script conforme implementado)
python getProduct.py

# coletar detalhes para produtos já listados
python getDetails.py
```

## Notas
- Alguns sites bloqueiam scraping: use uma API dedicada (como scrape.do) ou mecanismos de proxy/rotatividade se necessário.
- Pegue uma API Key com o scrape.do no site [https://scrape.do/](https://scrape.do/)