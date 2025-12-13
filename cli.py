#!/usr/bin/env python3
"""
Command-line interface for PDF processing
Quick tool for testing without running the full API server
"""

import sys
import argparse
from pathlib import Path
from pdf_processor import PDFProcessor
from summary_generator import SummaryGenerator


def main():
    parser = argparse.ArgumentParser(description='Process PDF documents')
    parser.add_argument('pdf_file', type=str, help='Path to PDF file')
    parser.add_argument('--no-summary', action='store_true', help='Skip summary generation')
    parser.add_argument('--dpi', type=int, default=300, help='Image resolution (default: 300)')

    args = parser.parse_args()

    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    if pdf_path.suffix.lower() != '.pdf':
        print("Error: File must be a PDF")
        sys.exit(1)

    print(f"Processing: {pdf_path.name}")
    print(f"Resolution: {args.dpi} DPI")
    print()

    processor = PDFProcessor()

    try:
        image_paths, zip_path = processor.process_pdf(str(pdf_path), dpi=args.dpi)

        print(f"✓ Converted {len(image_paths)} pages")
        print(f"✓ Images saved to: {Path(image_paths[0]).parent}")
        print(f"✓ ZIP archive: {zip_path}")
        print()

        if not args.no_summary:
            print("Generating summary...")
            try:
                summary_gen = SummaryGenerator()
                summary = summary_gen.generate_summary(str(pdf_path))
                print()
                print("McKinsey-Style Summary:")
                print("-" * 60)
                print(summary)
                print("-" * 60)
                print(f"Character count: {len(summary)}/200")
            except Exception as e:
                print(f"Summary generation failed: {e}")

    except Exception as e:
        print(f"Processing failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
