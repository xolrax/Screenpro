import os
import inspect
from dotenv import load_dotenv

ruta_archivo = os.path.abspath(inspect.getfile(inspect.currentframe()))
base_dir = os.path.dirname(ruta_archivo)

print(f"ruta de archivo : {base_dir}")