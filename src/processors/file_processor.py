"""
File Processor - Handles text extraction from PDFs and images
"""
import os
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image
import pytesseract
import pdfplumber
from pdf2image import convert_from_path
import PyPDF2


class FileProcessor:
    """Processes various file types and extracts text content"""

    SUPPORTED_IMAGE_FORMATS = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'}
    SUPPORTED_DOC_FORMATS = {'.pdf', '.txt'}

    def __init__(self):
        self.processed_files = []

    def is_supported_file(self, file_path: str) -> bool:
        """Check if file format is supported"""
        ext = Path(file_path).suffix.lower()
        return ext in (self.SUPPORTED_IMAGE_FORMATS | self.SUPPORTED_DOC_FORMATS)

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file for duplicate detection"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Perform OCR with Portuguese language support
            text = pytesseract.image_to_string(image, lang='por')
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from image {image_path}: {e}")
            return ""

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF (tries text extraction first, then OCR)"""
        text = ""

        # Try text extraction first (for PDFs with selectable text)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error with pdfplumber on {pdf_path}: {e}")

        # If no text extracted, try OCR on PDF images
        if not text.strip():
            try:
                images = convert_from_path(pdf_path)
                for i, image in enumerate(images):
                    page_text = pytesseract.image_to_string(image, lang='por')
                    text += page_text + "\n"
            except Exception as e:
                print(f"Error with OCR on PDF {pdf_path}: {e}")

        return text.strip()

    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from text file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except UnicodeDecodeError:
            # Try with latin-1 encoding if utf-8 fails
            try:
                with open(txt_path, 'r', encoding='latin-1') as f:
                    return f.read().strip()
            except Exception as e:
                print(f"Error reading text file {txt_path}: {e}")
                return ""
        except Exception as e:
            print(f"Error reading text file {txt_path}: {e}")
            return ""

    def process_file(self, file_path: str) -> Dict:
        """Process a single file and extract all information"""
        if not os.path.exists(file_path):
            return {
                'success': False,
                'error': 'File not found',
                'file_path': file_path
            }

        if not self.is_supported_file(file_path):
            return {
                'success': False,
                'error': 'Unsupported file format',
                'file_path': file_path
            }

        ext = Path(file_path).suffix.lower()
        file_name = Path(file_path).name
        file_size = os.path.getsize(file_path)

        # Calculate file hash
        file_hash = self.calculate_file_hash(file_path)

        # Extract text based on file type
        text = ""
        if ext in self.SUPPORTED_IMAGE_FORMATS:
            text = self.extract_text_from_image(file_path)
        elif ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif ext == '.txt':
            text = self.extract_text_from_txt(file_path)

        result = {
            'success': True,
            'file_path': file_path,
            'file_name': file_name,
            'file_extension': ext,
            'file_size': file_size,
            'file_hash': file_hash,
            'extracted_text': text,
            'text_length': len(text)
        }

        self.processed_files.append(result)
        return result

    def process_multiple_files(self, file_paths: List[str], progress_callback=None) -> List[Dict]:
        """Process multiple files with optional progress callback"""
        results = []
        total = len(file_paths)

        for i, file_path in enumerate(file_paths):
            result = self.process_file(file_path)
            results.append(result)

            if progress_callback:
                progress_callback(i + 1, total, file_path)

        return results
