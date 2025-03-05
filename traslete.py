import PyPDF2
from googletrans import Translator, LANGUAGES
import os
import re
from save import save_translated_text, save_translated_text_as_pdf

def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            full_text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            return full_text.strip()
    except FileNotFoundError:
        return "Error: PDF file not found at the specified path."
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def translate_text(text, target_language='en'):
    """Translate the given text to the target language but keep words in () unchanged."""
    try:
        translator = Translator()

        # Encontrar todas las palabras dentro de paréntesis
        matches = re.findall(r'\(.*?\)', text)

        # Reemplazar los textos dentro de () con un marcador temporal
        placeholders = {f"PLACEHOLDER_{i}": match for i, match in enumerate(matches)}
        for key, value in placeholders.items():
            text = text.replace(value, key)

        # Traducir el texto sin los paréntesis
        chunk_size = 5000  # Límite de caracteres de Google Translate
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        
        translated_chunks = []
        for chunk in chunks:
            translated = translator.translate(chunk, dest=target_language)
            translated_chunks.append(translated.text)

        translated_text = "\n".join(translated_chunks)

        # Restaurar las palabras dentro de paréntesis
        for key, value in placeholders.items():
            translated_text = translated_text.replace(key, value)

        return translated_text
    except Exception as e:
        return f"Error during translation: {str(e)}"

def translate_pdf(pdf_path, target_lang='en'):
    """Translate a PDF and save as a TXT and PDF file."""
    if not os.path.exists(pdf_path):
        print("Error: File does not exist.")
        return
    
    if target_lang not in LANGUAGES:
        print("Invalid language code. Defaulting to English.")
        target_lang = 'en'

    print(f"\nExtracting text from PDF: {pdf_path}")
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if extracted_text.startswith("Error"):
        print(extracted_text)
        return
    
    print(f"Translating text to {LANGUAGES[target_lang]} ({target_lang})...")
    translated_text = translate_text(extracted_text, target_lang)
    
    if translated_text.startswith("Error"):
        print(translated_text)
        return
    
    txt_path = save_translated_text(translated_text, pdf_path, target_lang)
    if "Error" in txt_path:
        print(txt_path)
        return

    pdf_result = save_translated_text_as_pdf(txt_path)
    print(pdf_result)
