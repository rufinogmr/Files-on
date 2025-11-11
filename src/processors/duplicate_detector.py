"""
Duplicate Detector - Finds duplicate files based on hash and content similarity
"""
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import imagehash
from PIL import Image
from difflib import SequenceMatcher


class DuplicateDetector:
    """Detects duplicate files using multiple strategies"""

    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize duplicate detector

        Args:
            similarity_threshold: Text similarity threshold (0.0 to 1.0)
        """
        self.similarity_threshold = similarity_threshold

    def find_exact_duplicates(self, processed_files: List[Dict]) -> Dict[str, List[Dict]]:
        """Find exact duplicates based on file hash"""
        hash_groups = defaultdict(list)

        for file_info in processed_files:
            if file_info.get('success'):
                file_hash = file_info.get('file_hash')
                hash_groups[file_hash].append(file_info)

        # Filter out unique files (only keep groups with 2+ files)
        duplicates = {
            hash_key: files
            for hash_key, files in hash_groups.items()
            if len(files) > 1
        }

        return duplicates

    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (0.0 to 1.0)"""
        if not text1 or not text2:
            return 0.0

        # Normalize texts
        text1_clean = ' '.join(text1.lower().split())
        text2_clean = ' '.join(text2.lower().split())

        return SequenceMatcher(None, text1_clean, text2_clean).ratio()

    def calculate_image_similarity(self, image_path1: str, image_path2: str) -> float:
        """Calculate perceptual similarity between two images"""
        try:
            hash1 = imagehash.average_hash(Image.open(image_path1))
            hash2 = imagehash.average_hash(Image.open(image_path2))

            # Calculate similarity (0 = identical, higher = more different)
            difference = hash1 - hash2
            # Convert to similarity score (0.0 to 1.0)
            similarity = 1.0 - (difference / 64.0)
            return max(0.0, similarity)
        except Exception as e:
            print(f"Error calculating image similarity: {e}")
            return 0.0

    def find_similar_files(self, processed_files: List[Dict]) -> List[Tuple[Dict, Dict, float]]:
        """Find similar files based on content similarity"""
        similar_pairs = []
        n = len(processed_files)

        for i in range(n):
            if not processed_files[i].get('success'):
                continue

            for j in range(i + 1, n):
                if not processed_files[j].get('success'):
                    continue

                file1 = processed_files[i]
                file2 = processed_files[j]

                # Skip if already exact duplicates (same hash)
                if file1['file_hash'] == file2['file_hash']:
                    continue

                # Calculate text similarity
                text1 = file1.get('extracted_text', '')
                text2 = file2.get('extracted_text', '')

                similarity = self.calculate_text_similarity(text1, text2)

                # For images, also check perceptual similarity
                if (file1['file_extension'] in {'.png', '.jpg', '.jpeg'} and
                    file2['file_extension'] in {'.png', '.jpg', '.jpeg'}):
                    image_similarity = self.calculate_image_similarity(
                        file1['file_path'],
                        file2['file_path']
                    )
                    # Take the maximum of text and image similarity
                    similarity = max(similarity, image_similarity)

                if similarity >= self.similarity_threshold:
                    similar_pairs.append((file1, file2, similarity))

        # Sort by similarity (highest first)
        similar_pairs.sort(key=lambda x: x[2], reverse=True)
        return similar_pairs

    def generate_duplicate_report(self, processed_files: List[Dict]) -> Dict:
        """Generate comprehensive duplicate detection report"""
        exact_duplicates = self.find_exact_duplicates(processed_files)
        similar_files = self.find_similar_files(processed_files)

        # Count statistics
        total_files = len([f for f in processed_files if f.get('success')])
        exact_duplicate_count = sum(len(files) - 1 for files in exact_duplicates.values())
        similar_file_count = len(similar_files)

        report = {
            'total_files': total_files,
            'exact_duplicates': exact_duplicates,
            'exact_duplicate_count': exact_duplicate_count,
            'similar_files': similar_files,
            'similar_file_count': similar_file_count,
            'unique_files': total_files - exact_duplicate_count
        }

        return report

    def get_files_to_keep(self, duplicate_groups: Dict[str, List[Dict]]) -> List[str]:
        """
        From duplicate groups, suggest which files to keep (first occurrence)
        Returns list of file paths to keep
        """
        files_to_keep = []

        for hash_key, files in duplicate_groups.items():
            if files:
                # Keep the first file (or could be based on other criteria)
                files_to_keep.append(files[0]['file_path'])

        return files_to_keep

    def get_files_to_remove(self, duplicate_groups: Dict[str, List[Dict]]) -> List[str]:
        """
        From duplicate groups, suggest which files to remove
        Returns list of file paths that are duplicates
        """
        files_to_remove = []

        for hash_key, files in duplicate_groups.items():
            if len(files) > 1:
                # Remove all except the first one
                for file_info in files[1:]:
                    files_to_remove.append(file_info['file_path'])

        return files_to_remove
