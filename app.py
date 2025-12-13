"""
PDF Document Processing API
Professional document conversion and summarization service
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from pdf_processor import PDFProcessor
from summary_generator import SummaryGenerator

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

processor = PDFProcessor()


def allowed_file(filename: str) -> bool:
    """Check if file is a PDF"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/process', methods=['POST'])
def process_document():
    """
    Process PDF document: convert to images, create ZIP, generate summary

    Returns:
        JSON with image URLs, ZIP URL, and Chinese summary
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are supported"}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)

    try:
        image_paths, zip_path = processor.process_pdf(upload_path)

        pdf_name = Path(upload_path).stem
        image_urls = [f"/download/image/{pdf_name}/{Path(img).name}" for img in image_paths]
        zip_url = f"/download/zip/{pdf_name}"

        try:
            summary_gen = SummaryGenerator()
            summary = summary_gen.generate_summary(upload_path, max_chars=200)
        except Exception as e:
            app.logger.warning(f"Summary generation failed: {e}")
            summary = "文档摘要生成暂时不可用"

        os.remove(upload_path)

        return jsonify({
            "status": "success",
            "total_pages": len(image_paths),
            "images": image_urls,
            "zip": zip_url,
            "summary": summary
        }), 200

    except Exception as e:
        app.logger.error(f"Processing error: {e}")
        if os.path.exists(upload_path):
            os.remove(upload_path)
        return jsonify({"error": "Processing failed"}), 500


@app.route('/download/image/<pdf_name>/<image_name>', methods=['GET'])
def download_image(pdf_name: str, image_name: str):
    """Download individual page image"""
    image_path = processor.output_dir / pdf_name / image_name

    if not image_path.exists():
        return jsonify({"error": "Image not found"}), 404

    return send_file(image_path, mimetype='image/png', as_attachment=True)


@app.route('/download/zip/<pdf_name>', methods=['GET'])
def download_zip(pdf_name: str):
    """Download ZIP archive of all images"""
    zip_path = processor.output_dir / pdf_name / f"{pdf_name}_images.zip"

    if not zip_path.exists():
        return jsonify({"error": "ZIP file not found"}), 404

    return send_file(
        zip_path,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{pdf_name}_images.zip"
    )


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({"error": "File size exceeds 50MB limit"}), 413


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
