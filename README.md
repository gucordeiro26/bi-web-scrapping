# 🚀 Pipeline de Análise de Sentimentos e Tópicos - E-commerce

Este repositório contém o pipeline completo de Engenharia de Dados e NLP para o **Par Temático 2: Análise de Sentimentos no E-commerce Brasileiro**. O objetivo do projeto é coletar, processar, analisar e persistir reviews de produtos de um grande varejista brasileiro (Casas Bahia).

O pipeline final processa os dados brutos e gera um banco de dados (`reviews.duckdb`) pronto para ser consumido por uma ferramenta de BI (como o Tableau) para análise gerencial.

## 📈 Pipeline de Processamento

O projeto é dividido em um pipeline de ponta a ponta:

1.  **Coleta de Dados (Scraping):** Os scripts em `src/scraping/` são responsáveis por coletar dados do site-alvo e salvar os comentários brutos.
2.  **Limpeza e Processamento:** O texto dos comentários é normalizado (acentos, caixa baixa, caracteres especiais) para preparar a análise.
3.  **Análise de Sentimento:** Um modelo híbrido (baseado em regras de nota e no léxico `LeIA`) classifica cada comentário como `Positivo`, `Negativo` ou `Neutro`.
4.  **Extração de Tópicos:** A biblioteca `spaCy` é usada para analisar os comentários e extrair os substantivos-chave (ex: "bateria", "tela", "entrega"), indicando *sobre o que* o cliente falou.
5.  **Persistência (Data Warehouse):** O resultado final (comentários, sentimentos e tópicos) é salvo em um banco de dados `DuckDB`, pronto para a análise de BI.

## 🗂️ Estrutura do Repositório

O projeto é organizado de forma modular para garantir a separação entre código-fonte, dados e notebooks de análise, conforme a estrutura final do projeto.

```
bi-web-scrapping/
├── .gitignore
├── README.md               <-- Este arquivo
├── requirements.txt        <-- Todas as dependências do projeto
│
├── data/
│   ├── raw/                <-- Dados brutos coletados (ex: comentarios_produtos.csv)
│   └── output/             <-- Saída do pipeline (ex: reviews.duckdb)
│
├── notebooks/
│   ├── 1-analise_sentimento_mvp.ipynb  <-- Entrega da Semana 2
│   └── 2-extracao_topicos_e_db.ipynb   <-- Entrega da Semana 3 (Pipeline Completo)
│
├── src/
│   ├── __init__.py
│   ├── processing/         <-- Módulo Python com toda a lógica de NLP e BD
│   │   ├── __init__.py
│   │   └── text_processor.py
│   └── scraping/           <-- Módulo Python com os scripts de coleta de dados
│       ├── __init__.py
│       ├── agents.py
│       ├── get_products.py
│       └── get_reviews.py
│
└── venv/                   <-- Ambiente virtual (ignorado pelo .gitignore)
```

## ⚙️ Como Configurar e Executar o Projeto

Siga estes passos para configurar o ambiente e executar o pipeline completo.

### 1. Pré-requisitos

* **Python:** Este projeto foi desenvolvido e testado com **Python 3.11**. Versões mais novas (como 3.13+) causam erros de incompatibilidade com as bibliotecas de dados.
* **Git:** Para clonar o repositório.
* **Habilitar Caminhos Longos no Windows:** Este projeto exige a instalação de pacotes com nomes de arquivo longos. É **obrigatório** habilitar o suporte a "Win32 Long Paths" no Windows.

### 2. Instalação

**Passo 1: Clonar o Repositório**
```bash
git clone [https://github.com/seu-usuario/bi-web-scrapping.git](https://github.com/seu-usuario/bi-web-scrapping.git)
cd bi-web-scrapping
```

**Passo 2: Criar e Ativar o Ambiente Virtual**
(É crucial usar o Python 3.11 para este comando)
```bash
# Cria o ambiente virtual
py -3.11 -m venv venv

# Ativa o ambiente (no terminal Bash do VS Code)
source venv/Scripts/activate

# (Se estiver usando o CMD Padrão do Windows, use: .\venv\Scripts\activate)
```

**Passo 3: Instalar todas as Dependências**
(Com o ambiente `(venv)` ativo)
```bash
# Instala todas as bibliotecas do projeto
pip install -r requirements.txt

# Instala a ferramenta Jupyter Notebook
pip install notebook
```

**Passo 4: Baixar o Modelo de NLP (spaCy)**
```bash
python -m spacy download pt_core_news_sm
```

### 3. Executando o Pipeline

O pipeline de processamento (Semanas 2 e 3) é executado através do notebook principal.

**Passo 1: Iniciar o Jupyter Notebook**
(Com o ambiente `(venv)` ativo)
```bash
# Comando mais robusto para iniciar o notebook
python -m notebook
```

**Passo 2: Executar o Notebook da Semana 3**
1.  No navegador que abrir, clique na pasta `notebooks/`.
2.  Abra o arquivo `2-extracao_topicos_e_db.ipynb`.
3.  **REINICIE O KERNEL:** Vá ao menu **"Kernel" > "Restart Kernel..."** (para garantir que todas as bibliotecas instaladas sejam carregadas).
4.  Execute todas as células do notebook, de cima para baixo.

### 4. Saída do Projeto

Após a execução bem-sucedida, o arquivo final **`reviews.duckdb`** estará disponível na pasta `data/output/`.

Este arquivo contém a tabela `reviews_classificadas` com todas as colunas, incluindo `sentimento` e `topicos`, pronta para ser conectada ao Tableau.