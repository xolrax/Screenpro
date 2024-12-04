import os

parametros = {}  # Diccionario para almacenar las variables

def cargar_parametros(base_dir, proyecto):
    global parametros
    base_dir_absoluto = os.path.abspath(os.path.join(os.getcwd(), os.pardir, base_dir))
    ruta_parametros = os.path.join(base_dir_absoluto, proyecto, f"{proyecto}.txt")

    if not os.path.exists(ruta_parametros):
        raise FileNotFoundError(f"No se encontró el archivo de parámetros: {ruta_parametros}")

    with open(ruta_parametros, 'r', encoding='utf-8') as file:
        for line in file:
            # Ignorar líneas vacías o comentarios completos
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Separar clave y valor, ignorando comentarios al final de la línea
            key_value = line.split("#")[0].strip()  # Eliminar el comentario
            key, value = map(str.strip, key_value.split('=', 1))
            
            # Quitar comillas del valor
            value = value.strip('"').strip("'")
            
            # Combinar ruta si es relativa
            if not os.path.isabs(value):
                value = os.path.join(base_dir_absoluto, proyecto, value)
            
            parametros[key] = value
