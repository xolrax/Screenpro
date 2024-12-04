import pandas as pd

def crea_contenido_pubmed(filepath):
    # Inicializar la lista para almacenar los datos extraídos
    contenido_pubmed = []

    # Leer el contenido del archivo
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()

    # Variables temporales para almacenar información de cada artículo
    current_article = {}

    for i, line in enumerate(lines):
        # Extraer PMID
        if line.startswith('PMID- '):
            current_article['PMID'] = line.split('- ')[1].strip()
        
        # Extraer DOI
        elif line.startswith('LID - ') and '[doi]' in line:
            current_article['DOI'] = line.split(' [doi]')[0].split('- ')[1].strip()
        
        # Extraer título del artículo
        elif line.startswith('TI  - '):
            title = line[6:].strip()
            # Continuar extrayendo el título si se extiende a múltiples líneas
            j = i + 1
            while j < len(lines) and lines[j].startswith('      '):
                title += ' ' + lines[j].strip()
                j += 1
            current_article['Title'] = title
        
        # Extraer Abstract
        elif line.startswith('AB  - '):
            abstract = line[6:].strip()
            j = i + 1
            while j < len(lines) and lines[j].startswith('      '):
                abstract += ' ' + lines[j].strip()
                j += 1
            current_article['Abstract'] = abstract

        # Extraer revista
        elif line.startswith('JT  - '):
            current_article['Journal'] = line[6:].strip()

        # Guardar y reiniciar para el próximo artículo al encontrar una línea vacía
        if line == '':
            if current_article:
                # Solo requerir que estén presentes 'PMID', 'Title' y 'Abstract'
                if all(key in current_article for key in ['PMID', 'Title', 'Abstract']):
                    contenido_pubmed.append([
                        current_article.get('Title', 'No Title'),
                        current_article.get('DOI', 'No DOI'),
                        current_article.get('PMID', 'No PMID'),
                        current_article.get('Journal', 'No Journal'),
                        current_article.get('Abstract', 'No Abstract')
                    ])
                # Reiniciar el diccionario para el siguiente artículo
                current_article = {}

    # Asegurarse de agregar el último artículo si el archivo no termina en una línea en blanco
    if current_article:
        if all(key in current_article for key in ['PMID', 'Title', 'Abstract']):
            contenido_pubmed.append([
                current_article.get('Title', 'No Title'),
                current_article.get('DOI', 'No DOI'),
                current_article.get('PMID', 'No PMID'),
                current_article.get('Journal', 'No Journal'),
                current_article.get('Abstract', 'No Abstract')
            ])

    # Convertir la lista a DataFrame
    df = pd.DataFrame(contenido_pubmed, columns=['Title', 'DOI', 'PMID', 'Journal', 'Abstract'])
    return df
