import re
import pandas as pd

def crea_contenido_scopus(filepath):
    """
    Procesa un archivo exportado de Scopus para extraer información de artículos, libros y conferencias.
    
    Entrada:
    - filepath: Ruta al archivo que contiene los datos de Scopus.

    Salida:
    - df: DataFrame con la información extraída de artículos, libros y conferencias.
    """
    # Leer todo el contenido del archivo
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Dividir el contenido en entradas de artículos, libros y conferencias
    entries = re.split(r'@(ARTICLE|BOOK|CONFERENCE)', content)
    
    # Preparar la lista para recolectar datos
    data = []

    # Iterar sobre cada entrada para extraer información
    for i in range(1, len(entries), 2):
        entry_type = entries[i]  # Puede ser ARTICLE, BOOK o CONFERENCE
        entry_content = entries[i+1]  # Contenido del artículo, libro o conferencia

        # Extraer campos comunes, modificando la expresión para que capture múltiples líneas y caracteres especiales dentro de las llaves
        title = re.search(r'title\s*=\s*\{(.*?)\}', entry_content, re.DOTALL)
        doi = re.search(r'doi\s*=\s*\{(.*?)\}', entry_content, re.DOTALL)
        pmid = re.search(r'PMID-\s*(\d+)', entry_content)
        journal = re.search(r'journal\s*=\s*\{(.*?)\}', entry_content, re.DOTALL)
        abstract = re.search(r'abstract\s*=\s*\{(.*?)\}', entry_content, re.DOTALL)

        # Extraer el texto de cada campo, si está presente
        title_text = title.group(1) if title else 'No Title'
        doi_text = doi.group(1) if doi else 'No DOI'
        pmid_text = pmid.group(1) if pmid else 'No PMID'
        journal_text = journal.group(1) if journal else 'No Journal'
        abstract_text = abstract.group(1) if abstract else 'No Abstract'
        
        # Añadir el tipo de entrada (ARTICLE, BOOK o CONFERENCE)
        data.append([entry_type, title_text, doi_text, pmid_text, journal_text, abstract_text])

    # Crear un DataFrame con los datos recolectados
    df = pd.DataFrame(data, columns=['Type', 'Title', 'DOI', 'PMID', 'Journal', 'Abstract'])
    
    return df
