import re
from unidecode import unidecode
from LeIA import SentimentIntensityAnalyzer

# Inicializa o analisador de sentimento uma única vez quando o módulo é importado.
# Isso é mais eficiente do que inicializá-lo toda vez que a função é chamada.
_s = SentimentIntensityAnalyzer()

# Lista de termos que forçam uma classificação positiva.
_termos_positivos_fortes = [
    'otima', 'otimo', 'excelente', 'perfeita', 'perfeito', 
    'maravilhosa', 'maravilhoso', 'adorei', 'amei', 'show', 'incrivel'
]

def limpar_texto(texto):
    """
    Realiza a limpeza e normalização de um texto: converte para minúsculas,
    remove acentos e caracteres não-alfabéticos.
    """
    texto = str(texto).lower()
    texto = unidecode(texto)
    texto = re.sub(r'[^a-z\s]', '', texto)
    return texto

def analisar_sentimento_texto(texto):
    """
    Usa a biblioteca LeIA para retornar a classificação de um texto.
    Retorna 'Positivo', 'Negativo' ou 'Neutro'.
    """
    score = _s.polarity_scores(texto)['compound']
    if score > 0.05:
        return 'Positivo'
    elif score < -0.05:
        return 'Negativo'
    else:
        return 'Neutro'

def classificar_sentimento(df):
    """
    Aplica a lógica de classificação de sentimento completa a um DataFrame.
    Retorna o DataFrame com uma nova coluna 'sentimento'.
    
    O DataFrame de entrada deve conter as colunas 'comentario_limpo' e 'rating_do_comentario'.
    """
    
    # Camada 1 e 2: Classificação híbrida inicial
    def classificar_hibrido(row):
        if row['rating_do_comentario'] >= 4:
            return 'Positivo'
        elif row['rating_do_comentario'] <= 2:
            return 'Negativo'
        else: # rating == 3
            return analisar_sentimento_texto(row['comentario_limpo'])

    df['sentimento_inicial'] = df.apply(classificar_hibrido, axis=1)

    # Camada 3: Correção de inconsistências
    def corrigir_negativos(row):
        if row['sentimento_inicial'] == 'Negativo':
            if any(termo in row['comentario_limpo'].split() for termo in _termos_positivos_fortes):
                return 'Positivo'
            if analisar_sentimento_texto(row['comentario_limpo']) == 'Positivo':
                return 'Positivo'
        return row['sentimento_inicial']

    df['sentimento'] = df.apply(corrigir_negativos, axis=1)
    df.drop(columns=['sentimento_inicial'], inplace=True)
    
    return df