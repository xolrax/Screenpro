import pandas as pd
from llm import quest_gpt

def screaning(df, lim=None, ruta_prompt=None):
    """
    Realiza el screening de artículos en un DataFrame basado en un prompt personalizado.

    Entrada:
    - df: DataFrame que contiene los artículos a evaluar.
    - lim: Rango de artículos a procesar (índice de inicio y fin).
    - ruta_prompt: Ruta del archivo que contiene el prompt base.

    Salida:
    - DataFrame actualizado con las columnas 'Traducción', 'Resumen', 'Inclusión' y 'Justificación'.
    """
    if ruta_prompt is None:
        raise ValueError("Se requiere una ruta al archivo del prompt para realizar el screening.")

    # Leer el contenido del archivo del prompt
    try:
        with open(ruta_prompt, 'r', encoding='utf-8') as file:
            prompt_base = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo del prompt en la ruta proporcionada: {ruta_prompt}")
    except Exception as e:
        raise Exception(f"Error al leer el archivo del prompt: {str(e)}")

    resultados = []
    inicio = lim[0] - 1 if lim else 0
    fin = lim[1] if lim else len(df)

    for index, row in df.iloc[inicio:fin].iterrows():
        # Construir el prompt completo concatenando el abstract del artículo
        prompt = (
            f"{prompt_base}\n\n"
            f"**Abstract del artículo a analizar:**\n"
            f"Abstract: {row['Abstract']}\n"
        )

        # Llamar a quest_gpt para procesar el prompt y obtener la respuesta
        respuesta_gpt = quest_gpt(prompt)

        # Extraer los datos desde la respuesta, adaptar según el formato específico que quest_gpt devuelve
        decision = respuesta_gpt.split("S1:")[1].split("\n")[0].strip()
        justificacion = respuesta_gpt.split("S2:")[1].split("\n")[0].strip()
        traduccion = respuesta_gpt.split("S3:")[1].split("\n")[0].strip()
        resumen = respuesta_gpt.split("S4:")[1].strip()

        resultados.append([traduccion, resumen, decision, justificacion])

    # Crear DataFrame de resultados
    resultados_df = pd.DataFrame(resultados, columns=['Traducción', 'Resumen', 'Inclusión', 'Justificación'])

    # Añadir resultados a la tabla original solo para el rango especificado
    df.loc[inicio:fin-1, ['Traducción', 'Resumen', 'Inclusión', 'Justificación']] = resultados_df.values

    return df

def screaning2(df, archivo_salida, inicio=1, paso=2, ruta_prompt=None):
    """
    Procesa artículos en bloques y guarda el progreso en un archivo Excel.

    Entrada:
    - df: DataFrame con los artículos.
    - archivo_salida: Ruta al archivo de salida.
    - inicio: Índice inicial del bloque a procesar.
    - paso: Tamaño del bloque a procesar.
    - ruta_prompt: Ruta al archivo que contiene el prompt base.
    """
    # Cargar el DataFrame existente si el archivo ya existe y el inicio es mayor que 1
    try:
        if inicio > 1:
            df = pd.read_excel(archivo_salida, index_col=None)
            print(f"Se cargó el DataFrame existente desde {archivo_salida}. Continuando desde el artículo {inicio}.")
        else:
            print("Iniciando desde el principio.")
    except FileNotFoundError:
        print("Archivo no encontrado, iniciando un nuevo proceso de evaluación.")

    total_articulos = len(df)
    
    # Procesar en bloques
    for i in range(inicio, total_articulos + 1, paso):
        fin = min(i + paso - 1, total_articulos)  # Asegurarse de no pasarse del rango
        print(f"Procesando artículos {i} a {fin}.")
        
        # Evaluar los artículos en el rango especificado
        df_actualizado = screaning(df, [i, fin], ruta_prompt=ruta_prompt)
        
        # Guardar el DataFrame en Excel
        df_actualizado.to_excel(archivo_salida, index=False)
        print(f"Datos guardados en {archivo_salida}. Progreso: Artículo {fin} de {total_articulos}.")

    print("Procesamiento completado.")
