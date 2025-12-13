# PDF Document Processor

Professional PDF to image conversion service with McKinsey-style Chinese summarization.

## Features

- **High-Quality Conversion**: Extract PDF pages as 300 DPI PNG images
- **Organized Output**: Images named by page number (page_001.png, page_002.png, etc.)
- **Batch Download**: Automatic ZIP archive creation for all images
- **AI Summarization**: McKinsey-style Chinese summaries (≤200 characters) using Claude
- **REST API**: Clean Flask-based API for document processing

## Installation

### Prerequisites

- Python 3.8+
- poppler-utils (for PDF processing)

#### Install poppler-utils

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Download from: https://github.com/oschwartz10612/poppler-windows/releases

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd codex_test
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### Start the Server

```bash
python app.py
```

Server runs on `http://localhost:5000`

### API Endpoints

#### 1. Process PDF Document

**Endpoint:** `POST /process`

**Request:**
```bash
curl -X POST \
  http://localhost:5000/process \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "success",
  "total_pages": 5,
  "images": [
    "/download/image/document/page_001.png",
    "/download/image/document/page_002.png",
    "/download/image/document/page_003.png",
    "/download/image/document/page_004.png",
    "/download/image/document/page_005.png"
  ],
  "zip": "/download/zip/document",
  "summary": "本报告深入分析数字化转型的关键驱动因素，揭示企业在技术采纳、组织变革和客户体验优化方面的核心挑战。数据显示，成功转型企业在创新投入上平均高出同行42%，且显著提升了市场响应速度。研究强调结构化方法论对于实现可持续增长的重要性。"
}
```

#### 2. Download Individual Image

**Endpoint:** `GET /download/image/<pdf_name>/<image_name>`

**Example:**
```bash
curl -O http://localhost:5000/download/image/document/page_001.png
```

#### 3. Download ZIP Archive

**Endpoint:** `GET /download/zip/<pdf_name>`

**Example:**
```bash
curl -O http://localhost:5000/download/zip/document
```

#### 4. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

## Architecture

```
codex_test/
├── app.py                  # Flask API server
├── pdf_processor.py        # PDF to image conversion
├── summary_generator.py    # AI-powered summarization
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── .gitignore             # Git ignore rules
└── README.md              # Documentation
```

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Required for summary generation

### File Limits

- Maximum upload size: 50MB
- Supported format: PDF only

## Development

### Core Modules

**PDFProcessor** (`pdf_processor.py`):
- Converts PDF pages to high-resolution PNG images
- Creates organized output directories
- Generates ZIP archives

**SummaryGenerator** (`summary_generator.py`):
- Analyzes PDF content using Claude vision
- Generates McKinsey-style summaries in Chinese
- Enforces 200-character limit

**Flask API** (`app.py`):
- Handles file uploads
- Orchestrates processing pipeline
- Provides download endpoints

## Design Principles

1. **Accuracy over Speed**: 300 DPI image quality, comprehensive error handling
2. **Clean Structure**: Modular architecture, clear separation of concerns
3. **Professional Tone**: Business-focused summaries, no marketing language

## License

MIT
