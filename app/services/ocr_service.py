import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image, ImageEnhance
import io
import time
import re
import os
import shutil
from app.config import settings

class OCRService:
    def __init__(self):
        tesseract_path = settings.TESSERACT_PATH
        if tesseract_path and os.path.isfile(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            detected_path = shutil.which("tesseract")
            if detected_path:
                pytesseract.pytesseract.tesseract_cmd = detected_path

    @staticmethod
    def preprocess_image(image: Image.Image) -> Image.Image:
        """Mejorar imagen para mejor OCR"""
        # Aumentar contraste
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)

        # Aumentar nitidez
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2)

        return image

    @staticmethod
    def fix_accents(text: str) -> str:
        """Corregir errores comunes de OCR con acentos"""

        # Reemplazar números confundidos con letras acentuadas
        replacements = {
            '6': 'ó',  # organizaci6n -> organización
            '0': 'o',  # n0 -> no (pero cuidado con números reales)
            '1': 'í',  # posi1ón -> posición
            '3': 'é',  # informaci3n -> información
            'l': 'í',  # capi1tal -> capital
        }

        # Patrones específicos más precisos
        patterns = {
            r'(\w)6n\b': r'\1ón',           # organizaci6n -> organización
            r'(\w)3n\b': r'\1én',           # informaci3n -> información
            r'(\w)1\b': r'\1í',             # posi1 -> posí
            r'(\w)n6s\b': r'\1nos',         # organizaci6nes -> organizaciones
            r'\ba\b': 'a',
            r'\bel\b': 'el',
            r'\blde\b': 'lde',
            r'rn': 'm',                     # captura errores "rn" por "m"
        }

        # Aplicar patrones regex primero
        for pattern, replacement in patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Diccionario de correcciones por palabra completa
        word_corrections = {
            r'\bIntroduccién\b': 'Introducción',
            r'\borganizaci6n\b': 'organización',
            r'\binforrnaci6n\b': 'información',
            r'\bconcluci6n\b': 'conclusión',
            r'\bdescripci6n\b': 'descripción',
            r'\binformaci3n\b': 'información',
            r'\bsituaci6n\b': 'situación',
            r'\bposici6n\b': 'posición',
            r'\bobjeci6n\b': 'objeción',
            r'\bexcepci6n\b': 'excepción',
            r'\bp3rdida\b': 'pérdida',
            r'\bdernrocracia\b': 'democracia',
            r'\bcélebre\b': 'célebre',
            r'\b3xito\b': 'éxito',
            r'\bp6blico\b': 'público',
            r'\bl1nea\b': 'línea',
            r'\bsiguiente\b': 'siguiente',
            r'\bprocedimiento\b': 'procedimiento',
            r'\bfundaci6n\b': 'fundación',
            r'\breuni6n\b': 'reunión',
            r'\bconstrucci6n\b': 'construcción',
            r'\bproducci6n\b': 'producción',
            r'\bsoluci6n\b': 'solución',
            r'\bdecisi6n\b': 'decisión',
            r'\btransici6n\b': 'transición',
            r'\bexpansi6n\b': 'expansión',
            r'\badquisici6n\b': 'adquisición',
        }

        for pattern, replacement in word_corrections.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Limpiar espacios múltiples
        text = re.sub(r'\n\n+', '\n\n', text)
        text = re.sub(r'  +', ' ', text)

        return text

    def extract_text_from_image(self, image_bytes: bytes) -> tuple[str, float, float]:
        try:
            start_time = time.time()
            image = Image.open(io.BytesIO(image_bytes))

            # Pre-procesar imagen
            image = self.preprocess_image(image)

            # Configuración mejorada de Tesseract para español
            config = '--psm 1 --oem 3'  # PSM 1 = detectar orientación, OEM 3 = mejor OCR
            text = pytesseract.image_to_string(image, lang='spa+eng', config=config)

            # Post-procesar para corregir acentos
            text = self.fix_accents(text)

            processing_time = time.time() - start_time
            confidence = 0.85 if text.strip() else 0.0
            return text, confidence, processing_time
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> tuple[str, float, float]:
        try:
            start_time = time.time()
            images = convert_from_bytes(pdf_bytes, dpi=300)  # Aumentar DPI para mejor calidad
            all_text = []

            config = '--psm 1 --oem 3'

            for image in images:
                # Pre-procesar imagen
                image = self.preprocess_image(image)
                text = pytesseract.image_to_string(image, lang='spa+eng', config=config)
                all_text.append(text)

            combined_text = "\n\n".join(all_text)

            # Post-procesar todo el texto
            combined_text = self.fix_accents(combined_text)

            processing_time = time.time() - start_time
            confidence = 0.85 if combined_text.strip() else 0.0
            return combined_text, confidence, processing_time
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def process_document(self, file_bytes: bytes, file_type: str) -> tuple[str, float, float]:
        file_type = file_type.lower()

        if file_type == "pdf":
            return self.extract_text_from_pdf(file_bytes)
        elif file_type in ["jpg", "jpeg", "png"]:
            return self.extract_text_from_image(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

ocr_service = OCRService()

