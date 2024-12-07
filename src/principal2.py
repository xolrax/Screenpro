
from contenido_pubmed import crea_contenido_pubmed
from contenido_scopus import crea_contenido_scopus
from procesamiento_tablas import fusionar_tablas, ordenar_por_titulo
from screaning import screaning, screaning2
from llm import cargar_api_key, quest_gpt
from cargar_parametros import cargar_parametros, parametros
import os
import inspect
from dotenv import load_dotenv


# Cargar las variables desde el archivo .env
load_dotenv()

####ACA CAMBIAR####
proyecto = "gemelos_digitales_cancer"
rutaapi=  "C:\\UNAB\\LLM\\Mi_Api.txt"
########################



# Determinar el directorio del archivo actual (donde está principal.py)
# Obtiene la ruta del archivo actual incluso si __file__ no está disponible
ruta_archivo = os.path.abspath(inspect.getfile(inspect.currentframe()))
base_dir = os.path.dirname(ruta_archivo)
# Ajustar el directorio base para revisiones
revisiones_dir = os.path.join(base_dir, "../revisiones")


cargar_parametros(revisiones_dir, proyecto)
cargar_api_key(rutaapi)
datos_pubmed = crea_contenido_pubmed(parametros['ruta_archivopub'])
datos_scopus = crea_contenido_scopus(parametros['ruta_archivoscopus'])
datos_fusionados = fusionar_tablas(datos_scopus, datos_pubmed)
datos_ordenados = ordenar_por_titulo(datos_fusionados)
screaning2(datos_ordenados, parametros['archivo_sal_screen'], 1,2, parametros['rutaprompt1'])

