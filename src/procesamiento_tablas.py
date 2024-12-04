import pandas as pd
def fusionar_tablas(df1, df2):
    """
    Fusiona dos DataFrames y elimina duplicados basados en 'Title', luego restablece el índice.

    Entrada:
    - df1: DataFrame con artículos de Scopus.
    - df2: DataFrame con artículos de PubMed.

    Salida:
    - DataFrame fusionado sin duplicados y con índice restablecido.
    """
    # Concatenar ambos DataFrames
    df_fusionado = pd.concat([df1, df2], ignore_index=True)

    # Eliminar duplicados basándose en la columna 'Title'
    df_fusionado = df_fusionado.drop_duplicates(subset=['Title'])

    # Restablecer el índice para que sea continuo
    df_fusionado.reset_index(drop=True, inplace=True)

    return df_fusionado
def ordenar_por_titulo(tabla_fusionada):
    """
    Esta función toma un DataFrame con artículos y los ordena alfabéticamente por el título,
    sin distinguir entre mayúsculas y minúsculas.

    Entrada:
    - tabla_fusionada: DataFrame con los artículos (debe tener una columna 'Title').

    Salida:
    - DataFrame ordenado alfabéticamente por el título.
    """
    # Ordenar el DataFrame por la columna 'Title' sin distinguir entre mayúsculas y minúsculas
    tabla_ordenada = tabla_fusionada.sort_values(by='Title', key=lambda x: x.str.lower(), ascending=True)
    
    # Reiniciar el índice para que sea continuo
    tabla_ordenada.reset_index(drop=True, inplace=True)
    
    return tabla_ordenada