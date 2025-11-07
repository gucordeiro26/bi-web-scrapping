import re
import pandas as pd
from unidecode import unidecode
from LeIA import SentimentIntensityAnalyzer
import spacy
from sqlalchemy import create_engine, text
import os

# --- CARREGAMENTO DOS MODELOS ---

try:
    _s = SentimentIntensityAnalyzer()
except Exception as e:
    print(f"Aviso: Não foi possível carregar o modelo LeIA. Erro: {e}")

try:
    _nlp = spacy.load("pt_core_news_sm", disable=["ner", "parser"])
except IOError:
    print("-------------------------------------------------------------------")
    print("Aviso: Modelo 'pt_core_news_sm' do spaCy não encontrado.")
    print("Por favor, execute a célula de instalação no notebook para baixá-lo.")
    print("-------------------------------------------------------------------")
    _nlp = None

# Lista de termos que forçam uma classificação positiva (para corrigir notas erradas)
_termos_positivos_fortes = [
    'otima', 'otimo', 'excelente', 'perfeita', 'perfeito', 
    'maravilhosa', 'maravilhoso', 'adorei', 'amei', 'show', 'incrivel'
]

# --- FUNÇÕES DE LIMPEZA E CLASSIFICAÇÃO ---

def limpar_texto(texto):
    """
    Realiza a limpeza e normalização de um texto: converte para minúsculas,
    remove acentos e caracteres não-alfabéticos.
    """
    texto = str(texto).lower()
    texto = unidecode(texto)
    texto = re.sub(r'[^a-z\s]', '', texto)
    return texto

def _analisar_sentimento_texto(texto):
    """Função interna para classificar um único texto."""
    score = _s.polarity_scores(texto)['compound']
    if score > 0.05:
        return 'Positivo'
    elif score < -0.05:
        return 'Negativo'
    else:
        return 'Neutro'

def classificar_sentimento(df):
    """
    Aplica a lógica de classificação de sentimento completa (híbrida) a um DataFrame.
    O DF de entrada deve conter 'comentario_limpo' e 'rating_do_comentario'.
    """
    
    # Camada 1 e 2: Classificação híbrida inicial
    def classificar_hibrido(row):
        if row['rating_do_comentario'] >= 4:
            return 'Positivo'
        elif row['rating_do_comentario'] <= 2:
            return 'Negativo'
        else: # rating == 3
            return _analisar_sentimento_texto(row['comentario_limpo'])

    df['sentimento_inicial'] = df.apply(classificar_hibrido, axis=1)

    # Camada 3: Correção de inconsistências (ex: nota 1, texto "ótimo")
    def corrigir_negativos(row):
        if row['sentimento_inicial'] == 'Negativo':
            if any(termo in row['comentario_limpo'].split() for termo in _termos_positivos_fortes):
                return 'Positivo'
            if _analisar_sentimento_texto(row['comentario_limpo']) == 'Positivo':
                return 'Positivo'
        return row['sentimento_inicial']

    df['sentimento'] = df.apply(corrigir_negativos, axis=1)
    df.drop(columns=['sentimento_inicial'], inplace=True)
    
    return df

def extrair_topicos(texto):
    """
    Processa um texto e extrai apenas os substantivos (tópicos).
    """
    if _nlp is None:
        print("Modelo spaCy não carregado. Pulando extração de tópicos.")
        return []
        
    doc = _nlp(texto)
    
    # Filtra palavras que são substantivos (NOUN) ou substantivos próprios (PROPN)
    # e que não sejam stopwords (palavras comuns como 'a', 'o', 'de').
    topicos = [
        token.text for token in doc 
        if (token.pos_ == "NOUN" or token.pos_ == "PROPN") and not token.is_stop
    ]
    
    # Retorna uma lista de tópicos únicos
    return list(set(topicos))

def salvar_no_banco_de_dados(df, db_path, table_name="reviews_classificadas"):
    """
    Salva o DataFrame final em um banco de dados DuckDB.
    Retorna (True, contagem_de_linhas) em caso de sucesso.
    Retorna (False, erro) em caso de falha.
    """
    try:
        # Garante que o diretório de saída exista
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        engine = create_engine(f"duckdb:///{db_path}")
        
        # Converte colunas de lista (como 'topicos') para string
        # Bando de dados SQL não armazena listas nativamente
        df_para_salvar = df.copy()
        if 'topicos' in df_para_salvar.columns:
            df_para_salvar['topicos'] = df_para_salvar['topicos'].astype(str)
            
        df_para_salvar.to_sql(table_name, engine, if_exists='replace', index=False)
        
        # Verificação
        with engine.connect() as conn:
            query = text(f"SELECT COUNT(*) FROM {table_name}")
            count = conn.execute(query).scalar()
        return True, count
        
    except Exception as e:
        return False, str(e)