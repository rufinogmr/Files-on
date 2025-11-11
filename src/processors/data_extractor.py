"""
Data Extractor - Extracts structured data (date, name, value) from receipts and documents
"""
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dateutil import parser as date_parser


class DataExtractor:
    """Extracts structured data from document text"""

    # Common Brazilian currency patterns
    CURRENCY_PATTERNS = [
        r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2}))',  # R$ 1.234,56
        r'R\$\s*(\d+,\d{2})',  # R$ 123,45
        r'(?:valor|total|pagamento|pago)[\s:]*R?\$?\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2}))',  # valor: 1.234,56
        r'(?:valor|total|pagamento|pago)[\s:]*R?\$?\s*(\d+,\d{2})',  # total: 123,45
    ]

    # Date patterns (Brazilian format)
    DATE_PATTERNS = [
        r'\b(\d{2})[/-](\d{2})[/-](\d{4})\b',  # DD/MM/YYYY or DD-MM-YYYY
        r'\b(\d{2})[/-](\d{2})[/-](\d{2})\b',  # DD/MM/YY or DD-MM-YY
        r'\b(\d{4})[/-](\d{2})[/-](\d{2})\b',  # YYYY/MM/DD or YYYY-MM-DD
    ]

    # Name patterns (common in receipts)
    NAME_PATTERNS = [
        r'(?:nome|cliente|beneficiário|favorecido)[\s:]+([A-ZÀ-Ú][A-Za-zÀ-úà-ú\s]{2,50})',
        r'(?:para|de|por)[\s:]+([A-ZÀ-Ú][A-Za-zÀ-úà-ú\s]{2,50})',
        r'^([A-ZÀ-Ú][A-Za-zÀ-úà-ú\s]{3,50})$',  # Capitalized name on its own line
    ]

    def __init__(self):
        pass

    def parse_brazilian_currency(self, value_str: str) -> float:
        """Convert Brazilian currency string to float"""
        # Remove R$ and whitespace
        value_str = value_str.replace('R$', '').strip()
        # Replace thousands separator (.) and decimal separator (,)
        value_str = value_str.replace('.', '').replace(',', '.')
        try:
            return float(value_str)
        except ValueError:
            return 0.0

    def extract_values(self, text: str) -> List[float]:
        """Extract all currency values from text"""
        values = []

        for pattern in self.CURRENCY_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get the captured group (the number part)
                value_str = match.group(1) if match.groups() else match.group(0)
                value = self.parse_brazilian_currency(value_str)
                if value > 0:
                    values.append(value)

        # Remove duplicates and sort
        values = sorted(list(set(values)), reverse=True)
        return values

    def extract_dates(self, text: str) -> List[datetime]:
        """Extract all dates from text"""
        dates = []

        for pattern in self.DATE_PATTERNS:
            matches = re.finditer(pattern, text)
            for match in matches:
                try:
                    date_str = match.group(0)
                    # Try to parse the date
                    parsed_date = date_parser.parse(date_str, dayfirst=True)
                    # Only accept dates that make sense (not too old or in the future)
                    current_year = datetime.now().year
                    if 1990 <= parsed_date.year <= current_year + 1:
                        dates.append(parsed_date)
                except (ValueError, OverflowError):
                    continue

        # Remove duplicates and sort (most recent first)
        dates = sorted(list(set(dates)), reverse=True)
        return dates

    def extract_names(self, text: str) -> List[str]:
        """Extract potential names from text"""
        names = []

        # Split text into lines for better name detection
        lines = text.split('\n')

        for pattern in self.NAME_PATTERNS:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                name = match.group(1).strip() if match.groups() else match.group(0).strip()
                # Clean up the name
                name = ' '.join(name.split())
                # Validate name (should have at least 3 chars and not be all numbers)
                if len(name) >= 3 and not name.isdigit() and not self._is_noise(name):
                    names.append(name)

        # Remove duplicates while preserving order
        seen = set()
        unique_names = []
        for name in names:
            name_lower = name.lower()
            if name_lower not in seen:
                seen.add(name_lower)
                unique_names.append(name)

        return unique_names[:5]  # Return top 5 names

    def _is_noise(self, text: str) -> bool:
        """Check if text is likely noise (not a real name)"""
        noise_words = {
            'data', 'valor', 'total', 'documento', 'comprovante', 'recibo',
            'nota', 'fiscal', 'pagamento', 'transação', 'cpf', 'cnpj',
            'endereço', 'telefone', 'email', 'site', 'www', 'http'
        }
        return text.lower() in noise_words

    def extract_data(self, text: str) -> Dict:
        """Extract all structured data from text"""
        values = self.extract_values(text)
        dates = self.extract_dates(text)
        names = self.extract_names(text)

        result = {
            'values': values,
            'primary_value': values[0] if values else None,
            'dates': dates,
            'primary_date': dates[0] if dates else None,
            'names': names,
            'primary_name': names[0] if names else None,
        }

        return result

    def extract_from_multiple_files(self, processed_files: List[Dict]) -> List[Dict]:
        """Extract data from multiple processed files"""
        results = []

        for file_info in processed_files:
            if not file_info.get('success'):
                results.append({
                    'file_path': file_info.get('file_path'),
                    'success': False,
                    'error': file_info.get('error')
                })
                continue

            text = file_info.get('extracted_text', '')
            extracted_data = self.extract_data(text)

            result = {
                'file_path': file_info['file_path'],
                'file_name': file_info['file_name'],
                'success': True,
                'extracted_data': extracted_data
            }

            results.append(result)

        return results

    def format_value(self, value: float) -> str:
        """Format float value as Brazilian currency string"""
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    def format_date(self, date: datetime) -> str:
        """Format datetime as Brazilian date string"""
        return date.strftime('%d/%m/%Y')

    def get_summary(self, extracted_data: Dict) -> str:
        """Get a human-readable summary of extracted data"""
        parts = []

        if extracted_data.get('primary_date'):
            parts.append(f"Data: {self.format_date(extracted_data['primary_date'])}")

        if extracted_data.get('primary_name'):
            parts.append(f"Nome: {extracted_data['primary_name']}")

        if extracted_data.get('primary_value'):
            parts.append(f"Valor: {self.format_value(extracted_data['primary_value'])}")

        return " | ".join(parts) if parts else "Nenhum dado extraído"
