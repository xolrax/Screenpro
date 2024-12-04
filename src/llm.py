from openai import OpenAI
global API_KEY

def cargar_api_key(api_key_path):
    """
    Carga la clave de la API desde un archivo y la almacena en la variable global.
    """
    global API_KEY
    try:
        with open(api_key_path, 'r', encoding='utf-8') as file:
            API_KEY = file.read().strip()
    except FileNotFoundError:
        raise Exception(f"No se encontró el archivo en la ruta proporcionada: {api_key_path}")
    except Exception as e:
        raise Exception(f"Error al leer la clave de la API: {str(e)}")


def quest_gpt(textin):
    """
    Esta función interactúa con la API de OpenAI para generar respuestas utilizando el modelo gpt-3.5-turbo.
    
    Entrada:
    - textin: String con el contenido del mensaje que se enviará al modelo.

    Salida:
    - varout: String con la respuesta generada por el modelo.
    """
    client = OpenAI(api_key=API_KEY) 
    response = client.chat.completions.create(
    #model="gpt-3.5-turbo",
    model="gpt-4o-mini",
    messages=[
    #{"role": "system", "content": "Toma conocimiento que David Araya es un ingeniero que trabaja en el ITISB"},
    {"role": "user", "content": textin}
    ]
    )
    choice = response.choices[0]
    varout=choice.message.content
    return varout
# Extrae contenido total