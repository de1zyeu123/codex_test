"""
McKinsey-Style Chinese Summary Generator
Generates professional, concise summaries for blog content
"""

import os
from typing import Optional
from anthropic import Anthropic
from pdf2image import convert_from_path


class SummaryGenerator:
    """Generates McKinsey-style Chinese summaries from PDF documents"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
        self.client = Anthropic(api_key=self.api_key)

    def generate_summary(self, pdf_path: str, max_chars: int = 200) -> str:
        """
        Generate a concise Chinese summary of PDF content

        Args:
            pdf_path: Path to PDF file
            max_chars: Maximum character count (default: 200)

        Returns:
            McKinsey-style Chinese summary
        """
        images = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=3)

        import base64
        import io

        image_content = []
        for idx, img in enumerate(images[:3]):
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode()

            image_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": img_base64
                }
            })

        prompt = f"""分析这份文档，生成一个专业的麦肯锡风格中文摘要，要求：

1. 字数限制：严格不超过{max_chars}个中文字符
2. 风格要求：
   - 采用麦肯锡式的结构化表达
   - 突出核心洞察和关键发现
   - 使用简洁、专业的商业语言
   - 避免营销性语言
3. 内容要求：
   - 聚焦文档的核心价值和主要观点
   - 适合博客文章使用
   - 数据驱动，事实为本

请直接输出摘要内容，不要任何额外说明。"""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{
                "role": "user",
                "content": image_content + [{"type": "text", "text": prompt}]
            }]
        )

        summary = message.content[0].text.strip()

        if len(summary) > max_chars:
            summary = summary[:max_chars-3] + "..."

        return summary
