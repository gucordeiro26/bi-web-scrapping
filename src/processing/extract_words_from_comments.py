import pandas as pd
import os
import re
from pathlib import Path

def extract_words(text):
    """
    Extrai palavras de um texto, removendo pontuação e convertendo para minúsculas.
    
    Args:
        text (str): Texto para extrair palavras
        
    Returns:
        list: Lista de palavras
    """
    if not isinstance(text, str):
        return []
    
    # Remove pontuação e converte para minúsculas
    text = text.lower()
    # Remove pontuação mantendo apenas letras, números e espaços
    text = re.sub(r'[^a-záéíóúãõçà\s]', '', text)
    # Divide o texto em palavras
    words = text.split()
    # Remove palavras vazias
    words = [w for w in words if w]
    
    return words


def process_comments():
    """
    Processa o arquivo de comentários classificados e cria dois CSVs:
    - palavras_positivas.csv: palavras dos comentários positivos
    - palavras_negativas.csv: palavras dos comentários negativos
    """
    
    # Caminho do arquivo de entrada
    input_file = Path(__file__).parent.parent.parent / "data" / "output" / "comentarios_classificados.csv"
    
    # Caminho dos arquivos de saída
    output_dir = Path(__file__).parent.parent.parent / "data" / "output"
    positive_output = output_dir / "palavras_positivas.csv"
    negative_output = output_dir / "palavras_negativas.csv"
    
    # Verificar se o arquivo de entrada existe
    if not input_file.exists():
        print(f"Erro: Arquivo não encontrado: {input_file}")
        return
    
    # Ler o CSV com separador pipe
    print(f"Lendo arquivo: {input_file}")
    df = pd.read_csv(input_file, sep='|')
    
    # Separar comentários positivos e negativos
    positive_comments = df[df['sentimento'] == 'Positivo']
    negative_comments = df[df['sentimento'] == 'Negativo']
    
    print(f"Total de comentários positivos: {len(positive_comments)}")
    print(f"Total de comentários negativos: {len(negative_comments)}")
    
    # Processar comentários positivos
    positive_data = []
    for idx, row in positive_comments.iterrows():
        id_comentario = row['id_comentario']
        texto = row['comentario_about_produto']
        palavras = extract_words(texto)
        
        for palavra in palavras:
            positive_data.append({
                'palavra': palavra,
                'id_comentario': id_comentario
            })
    
    # Processar comentários negativos
    negative_data = []
    for idx, row in negative_comments.iterrows():
        id_comentario = row['id_comentario']
        texto = row['comentario_about_produto']
        palavras = extract_words(texto)
        
        for palavra in palavras:
            negative_data.append({
                'palavra': palavra,
                'id_comentario': id_comentario
            })
    
    # Criar DataFrames e salvar como CSV
    positive_df = pd.DataFrame(positive_data)
    negative_df = pd.DataFrame(negative_data)
    
    # Salvar CSVs
    positive_df.to_csv(positive_output, index=False, sep=',')
    negative_df.to_csv(negative_output, index=False, sep=',')
    
    print(f"\nTotal de palavras extraídas:")
    print(f"  Positivas: {len(positive_df)}")
    print(f"  Negativas: {len(negative_df)}")
    
    print(f"\nArquivos gerados com sucesso:")
    print(f"  {positive_output}")
    print(f"  {negative_output}")


if __name__ == "__main__":
    process_comments()
