"""
Processors package - File processing and analysis modules
"""
from .file_processor import FileProcessor
from .duplicate_detector import DuplicateDetector
from .data_extractor import DataExtractor

__all__ = ['FileProcessor', 'DuplicateDetector', 'DataExtractor']
