import os
import pandas as pd
from rapidfuzz import process


def asociar_y_renombrar_archivos(carpeta, data):
    """Asocia y verifica archivos PDF en una carpeta
    con base en un DataFrame de correlativos y nombres de documentos.

    Args:
    carpeta (str): Ruta de la carpeta que contiene los archivos PDF.
    data (pd.DataFrame): DataFrame con columnas 'n' (correlativo) y 'nom_doc' (nombre de documentos).

    Returns:
    dict: Diccionario con:
        - 'numeric_not_associated': Archivos numéricos no asociados.
        - 'textual_not_associated': Archivos textuales no asociados.
        - 'missing_associations': Entradas de data sin archivo PDF asociado.
    """
    # Listas para guardar archivos no asociados
    not_associated_numeric = []
    not_associated_textual = []

    # Leer nombres de archivos en la carpeta
    pdf_files = [f for f in os.listdir(carpeta) if f.endswith('.pdf')]

    # Clasificar archivos
    numeric_files = [f for f in pdf_files if f.split('.')[0].isdigit()]
    text_files = [f for f in pdf_files if not f.split('.')[0].isdigit()]

    # Verificar archivos numéricos
    for file in numeric_files:
        num = int(file.split('.')[0])
        if num not in data['n'].values:
            not_associated_numeric.append(file)

    # Renombrar archivos textuales con coincidencia aproximada (fuzzy matching)
    for file in text_files:
        file_name = file.split('.pdf')[0]
        match = process.extractOne(file_name, data['nom_doc'], score_cutoff=80)
        if match:
            matched_doc = match[0]
            matched_n = data.loc[data['nom_doc'] == matched_doc, 'n'].values[0]
            new_name = f"{matched_n}.pdf"
            os.rename(os.path.join(carpeta, file), os.path.join(carpeta, new_name))
        else:
            not_associated_textual.append(file)

    # Verificar asociaciones completas
    archivos_actuales = [f.split('.pdf')[0] for f in os.listdir(carpeta) if f.endswith('.pdf')]
    missing_associations = data[~data['n'].astype(str).isin(archivos_actuales)]

    return {
        "numeric_not_associated": not_associated_numeric,
        "textual_not_associated": not_associated_textual,
        "missing_associations": missing_associations
    }

def imprimir_resultado(resultado):
    """Imprime los resultados del proceso de asociación
       y renombramiento de archivos.
       Args:
       resultado (dict): Diccionario devuelto por la función
       asociar_y_renombrar_archivos.
    """

    if resultado["numeric_not_associated"]:
        print("Archivos numéricos no asociados:")
        for file in resultado["numeric_not_associated"]:
            print(f" - {file}")
    else:
        print("Todos los archivos numéricos fueron asociados correctamente.")

    if resultado["textual_not_associated"]:
        print("\nArchivos textuales no asociados:")
        for file in resultado["textual_not_associated"]:
            print(f" - {file}")
    else:
        print("\nTodos los archivos textuales fueron asociados correctamente.")

    if not resultado["missing_associations"].empty:
        print("\nNombres en el DataFrame sin archivo PDF asociado:")
        print(resultado["missing_associations"])
    else:
        print("\nTodos los nombres del DataFrame tienen un archivo PDF asociado.")

# Ejemplo de DataFrame
data = pd.DataFrame({
    "n": [1, 2, 3],
    "nom_doc": ["Informe Anual", "Reporte Mensual", "Resumen Ejecutivo"]
})
#data = pd.read_clipboard()

# Ruta de la carpeta
carpeta = r"C:\Users\xalve\Desktop\Ej_PDF\Ej_pdf2"

# Ejecutar funciones
resultado = asociar_y_renombrar_archivos(carpeta, data)
imprimir_resultado(resultado)        

