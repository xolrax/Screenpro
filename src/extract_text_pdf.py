import fitz  # PyMuPDF
import json

def extract_text_with_details(pdf_path):
    """
    Extrae líneas de texto de un archivo PDF junto con sus detalles como tipo de fuente, tamaño y color, 
    procesando solo los bloques que contengan texto.

    Args:
        pdf_path (str): Ruta al archivo PDF.

    Returns:
        list: Lista de detalles de texto, donde cada entrada contiene:
            - page (int): Número de la página.
            - block_bbox (list): Área delimitadora (bounding box) del bloque (x0, y0, x1, y1).
            - line_bbox (list): Posición de la línea (x0, y0, x1, y1).
            - text (str): Texto del span.
            - font (str): Tipo de fuente.
            - size (float): Tamaño de la fuente.
            - color (int): Color del texto.
            - char_count (int): Contador de caracteres acumulado.
    """
    try:
        text_details = []
        char_count = 0  # Contador de caracteres incremental

        # Abre el documento PDF con un contexto
        with fitz.open(pdf_path) as pdf_document:
            # Itera sobre todas las páginas
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text_dict = page.get_text("dict")  # Obtiene el texto estructurado como diccionario
                
                for block in text_dict.get("blocks", []):
                    # Procesa solo los bloques que contengan texto y no imágenes u otros elementos
                    if block.get("type", 0) == 0:
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):  # Itera sobre fragmentos (spans)
                                char_count += len(span["text"])  # Incrementa el contador de caracteres
                                detail = {
                                    "page": page_num + 1,
                                    "block_bbox": block["bbox"],  # Área delimitadora (bounding box) del bloque (x0, y0, x1, y1)
                                    "line_bbox": line["bbox"],    # Posición de la línea
                                    "text": span["text"],         # Texto del span
                                    "font": span["font"],         # Tipo de fuente
                                    "size": span["size"],         # Tamaño de la fuente
                                    "color": span["color"],       # Color del texto
                                    "char_count": char_count       # Contador de caracteres acumulado
                                }
                                text_details.append(detail)

        return text_details

    except (FileNotFoundError, ValueError, TypeError) as e:
        print(f"Error al procesar el PDF: {e}")
        return None

def extract_text_with_details_block(pdf_path):
    """
    Extrae líneas de texto de un archivo PDF, procesando solo los bloques que contengan texto.

    Args:
        pdf_path (str): Ruta al archivo PDF.

    Returns:
        list: Lista de detalles de texto, donde cada entrada contiene:
            - page (int): Número de la página.
            - block_bbox (float): Coordenada y0 del bloque.
            - text (str): Texto del bloque.
            - char_count (int): Contador de caracteres acumulado.
    """
    try:
        text_details = []
        char_count = 0  # Contador de caracteres incremental

        # Abre el documento PDF con un contexto
        with fitz.open(pdf_path) as pdf_document:
            # Itera sobre todas las páginas
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text_blocks = page.get_text("blocks")  # Obtiene el texto estructurado como bloques
                
                for block in text_blocks:
                    # Desempaqueta los valores del bloque
                    block_bbox, block_text = block[1], block[4]
                    # Procesa solo los bloques que contengan texto y no imágenes u otros elementos
                    if block_text:
                        char_count += len(block_text)  # Incrementa el contador de caracteres
                        detail = {
                            "page": page_num + 1,
                            "block_bbox": block_bbox,  # Coordenada y0 del bloque
                            "text": block_text,        # Texto del bloque
                            "char_count": char_count   # Contador de caracteres acumulado
                        }
                        text_details.append(detail)

        return text_details

    except (FileNotFoundError, ValueError, TypeError) as e:
        print(f"Error al procesar el PDF: {e}")
        return None

def save_text_details_to_json(text_details, output_path):
    """
    Guarda la lista de detalles de texto en un archivo JSON.

    Args:
        text_details (list): Lista de detalles de texto.
        output_path (str): Ruta para guardar el archivo JSON.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(text_details, json_file, ensure_ascii=False, indent=4)
    except (OSError, TypeError) as e:
        print(f"Error al guardar el archivo JSON: {e}")

# # Ejemplo de uso
# def main():
#     pdf_path = r"C:\Users\xalve\Desktop\Ej_PDF\Liquidación.pdf"
#     output_json_path1 = r"C:\Users\xalve\Desktop\Ej_PDF\details.json"
#     output_json_path2 = r"C:\Users\xalve\Desktop\Ej_PDF\details_block.json"

#     text_details1 = extract_text_with_details(pdf_path)
#     text_details2 = extract_text_with_details_block(pdf_path)
#     if text_details1:
#         save_text_details_to_json(text_details1, output_json_path1)
#     if text_details2:
#         save_text_details_to_json(text_details2, output_json_path2)
# if __name__ == "__main__":
#     main()
