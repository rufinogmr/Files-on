"""
Suggestion Engine - Generates file name and folder organization suggestions
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from collections import defaultdict


class SuggestionEngine:
    """Generates intelligent suggestions for file naming and organization"""

    def __init__(self):
        pass

    def sanitize_filename(self, name: str) -> str:
        """Remove invalid characters from filename"""
        # Remove invalid characters
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        # Replace multiple spaces with single space
        name = re.sub(r'\s+', ' ', name)
        # Remove leading/trailing spaces
        name = name.strip()
        # Limit length
        if len(name) > 100:
            name = name[:100]
        return name

    def generate_filename(self, extracted_data: Dict, original_filename: str) -> str:
        """
        Generate a suggested filename based on extracted data
        Format: YYYY-MM-DD_Name_Value.ext
        """
        parts = []

        # Add date
        if extracted_data.get('primary_date'):
            date = extracted_data['primary_date']
            parts.append(date.strftime('%Y-%m-%d'))

        # Add name (sanitized and shortened)
        if extracted_data.get('primary_name'):
            name = extracted_data['primary_name']
            # Take first and last name only
            name_parts = name.split()
            if len(name_parts) > 2:
                name = f"{name_parts[0]} {name_parts[-1]}"
            name = self.sanitize_filename(name)
            parts.append(name)

        # Add value
        if extracted_data.get('primary_value'):
            value = extracted_data['primary_value']
            value_str = f"R${value:.2f}".replace('.', ',')
            parts.append(value_str)

        # If no data extracted, use original filename
        if not parts:
            return original_filename

        # Join parts and add original extension
        ext = Path(original_filename).suffix
        suggested_name = "_".join(parts) + ext

        return suggested_name

    def suggest_folder_structure(self, extraction_results: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Suggest folder organization based on extracted data
        Organizes by Year/Month
        """
        folder_structure = defaultdict(list)

        for result in extraction_results:
            if not result.get('success'):
                # Put unsuccessful extractions in "Unprocessed" folder
                folder_structure['Sem_Classificacao'].append(result)
                continue

            extracted_data = result.get('extracted_data', {})
            primary_date = extracted_data.get('primary_date')

            if primary_date:
                # Organize by Year/Month
                year = primary_date.strftime('%Y')
                month = primary_date.strftime('%m_%B')  # 01_January
                folder_path = f"{year}/{month}"
            else:
                # No date found - put in "Sem_Data" folder
                folder_path = "Sem_Data"

            folder_structure[folder_path].append(result)

        return dict(folder_structure)

    def suggest_category_structure(self, extraction_results: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Suggest folder organization by value categories
        Example: Baixo_Valor (<R$100), Medio_Valor (R$100-R$1000), Alto_Valor (>R$1000)
        """
        folder_structure = defaultdict(list)

        for result in extraction_results:
            if not result.get('success'):
                folder_structure['Sem_Classificacao'].append(result)
                continue

            extracted_data = result.get('extracted_data', {})
            primary_value = extracted_data.get('primary_value')

            if primary_value:
                if primary_value < 100:
                    category = "Baixo_Valor_ate_R$100"
                elif primary_value < 1000:
                    category = "Medio_Valor_R$100-R$1000"
                else:
                    category = "Alto_Valor_acima_R$1000"
            else:
                category = "Sem_Valor"

            folder_structure[category].append(result)

        return dict(folder_structure)

    def generate_organization_plan(self, extraction_results: List[Dict], output_dir: str) -> List[Dict]:
        """
        Generate a complete organization plan with:
        - Original file path
        - Suggested new filename
        - Suggested folder path
        - Full new path
        """
        organization_plan = []

        # Get folder structure suggestions (by date)
        folder_structure = self.suggest_folder_structure(extraction_results)

        for folder_path, files in folder_structure.items():
            for file_result in files:
                original_path = file_result['file_path']
                original_filename = file_result['file_name']

                # Generate new filename
                extracted_data = file_result.get('extracted_data', {})
                new_filename = self.generate_filename(extracted_data, original_filename)

                # Build full new path
                full_folder_path = os.path.join(output_dir, folder_path)
                full_new_path = os.path.join(full_folder_path, new_filename)

                # Handle filename conflicts
                counter = 1
                base_name = Path(new_filename).stem
                extension = Path(new_filename).suffix
                while os.path.exists(full_new_path) and full_new_path != original_path:
                    new_filename = f"{base_name}_{counter}{extension}"
                    full_new_path = os.path.join(full_folder_path, new_filename)
                    counter += 1

                plan_item = {
                    'original_path': original_path,
                    'original_filename': original_filename,
                    'suggested_filename': new_filename,
                    'suggested_folder': folder_path,
                    'full_folder_path': full_folder_path,
                    'full_new_path': full_new_path,
                    'extracted_data': extracted_data
                }

                organization_plan.append(plan_item)

        return organization_plan

    def get_organization_summary(self, organization_plan: List[Dict]) -> Dict:
        """Generate summary statistics for organization plan"""
        folders = set()
        renamed_count = 0

        for item in organization_plan:
            folders.add(item['suggested_folder'])
            if item['original_filename'] != item['suggested_filename']:
                renamed_count += 1

        summary = {
            'total_files': len(organization_plan),
            'total_folders': len(folders),
            'files_to_rename': renamed_count,
            'folders_list': sorted(list(folders))
        }

        return summary

    def execute_organization_plan(self, organization_plan: List[Dict],
                                  copy_files: bool = True) -> List[Dict]:
        """
        Execute the organization plan by moving/copying files

        Args:
            organization_plan: The plan to execute
            copy_files: If True, copy files; if False, move files

        Returns:
            List of results for each file operation
        """
        import shutil

        results = []

        for item in organization_plan:
            try:
                original_path = item['original_path']
                full_new_path = item['full_new_path']
                full_folder_path = item['full_folder_path']

                # Create directory if it doesn't exist
                os.makedirs(full_folder_path, exist_ok=True)

                # Copy or move file
                if copy_files:
                    shutil.copy2(original_path, full_new_path)
                    operation = 'copied'
                else:
                    shutil.move(original_path, full_new_path)
                    operation = 'moved'

                results.append({
                    'success': True,
                    'original_path': original_path,
                    'new_path': full_new_path,
                    'operation': operation
                })

            except Exception as e:
                results.append({
                    'success': False,
                    'original_path': item['original_path'],
                    'error': str(e)
                })

        return results
