import os
from reportlab.pdfgen import canvas

def save_translated_text(translated_text, original_path, target_language):
    """Save the translated text to a new TXT file."""
    try:
        base_name = os.path.splitext(original_path)[0]
        output_txt_path = f"{base_name}_translated_{target_language}.txt"

        with open(output_txt_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)

        return output_txt_path  # Devolver la ruta del archivo TXT
    except Exception as e:
        return f"Error saving file: {str(e)}"

def save_translated_text_as_pdf(txt_path):
    """Convert a translated TXT file into a PDF."""
    try:
        base_name = os.path.splitext(txt_path)[0]
        output_pdf_path = f"{base_name}.pdf"

        with open(txt_path, "r", encoding="utf-8") as file:
            text = file.readlines()

        c = canvas.Canvas(output_pdf_path)
        c.setFont("Helvetica", 12)

        # Ajustar el texto para que quepa en el PDF
        max_chars_per_line = 90
        y_position = 800

        for line in text:
            while len(line) > max_chars_per_line:
                c.drawString(50, y_position, line[:max_chars_per_line])
                line = line[max_chars_per_line:]
                y_position -= 20

                if y_position < 50:  # Nueva página si se llena
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = 800

            c.drawString(50, y_position, line.strip())
            y_position -= 20

            if y_position < 50:  # Nueva página si se llena
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = 800

        c.save()
        return f"Translation saved as PDF: {output_pdf_path}"
    except Exception as e:
        return f"Error saving PDF file: {str(e)}"
