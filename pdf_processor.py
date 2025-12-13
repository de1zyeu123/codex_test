"""
PDF Document Processor
Converts PDF pages to images with professional accuracy
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple
from pdf2image import convert_from_path
from PIL import Image
import zipfile


class PDFProcessor:
    """Handles PDF to image conversion and export operations"""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def process_pdf(self, pdf_path: str, dpi: int = 300) -> Tuple[List[str], str]:
        """
        Convert PDF to images and create ZIP archive

        Args:
            pdf_path: Path to PDF file
            dpi: Image resolution (default: 300 for high quality)

        Returns:
            Tuple of (list of image paths, zip file path)
        """
        pdf_name = Path(pdf_path).stem
        session_dir = self.output_dir / pdf_name

        if session_dir.exists():
            shutil.rmtree(session_dir)
        session_dir.mkdir(parents=True)

        images = convert_from_path(pdf_path, dpi=dpi)
        image_paths = []

        for page_num, image in enumerate(images, start=1):
            image_filename = f"page_{page_num:03d}.png"
            image_path = session_dir / image_filename
            image.save(image_path, "PNG", optimize=True)
            image_paths.append(str(image_path))

        zip_path = self._create_zip(session_dir, image_paths, pdf_name)

        return image_paths, zip_path

    def _create_zip(self, session_dir: Path, image_paths: List[str], pdf_name: str) -> str:
        """Create ZIP archive of all images"""
        zip_path = session_dir / f"{pdf_name}_images.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for image_path in image_paths:
                arcname = Path(image_path).name
                zipf.write(image_path, arcname)

        return str(zip_path)

    def get_page_count(self, pdf_path: str) -> int:
        """Get total number of pages in PDF"""
        images = convert_from_path(pdf_path, dpi=72, first_page=1, last_page=1)
        return len(images)

    def cleanup_session(self, pdf_name: str):
        """Remove session directory and all files"""
        session_dir = self.output_dir / pdf_name
        if session_dir.exists():
            shutil.rmtree(session_dir)
