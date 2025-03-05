import PyPDF2
from googletrans import Translator, LANGUAGES
import os
from save import save_translated_text
from traslete  import *



if __name__ == "__main__":
    # Instalación automática de paquetes si no están presentes
    try:
        import PyPDF2
        import googletrans
    except ImportError:
        print("Installing required packages...")
        os.system("pip install PyPDF2 googletrans==3.1.0a0")
    
    print("PDF Translation System")
    print("---------------------")
    
    # DEFINE AQUÍ EL PATH DEL PDF Y EL IDIOMA DESTINO
    pdf_file_path = r"YOUR_PATH"  # Cambia esta ruta por la del PDF real
    target_language = "es"  # Cambia el código de idioma según necesites ('fr' para francés, 'de' para alemán, etc.)
    
    translate_pdf(pdf_file_path, target_language)
