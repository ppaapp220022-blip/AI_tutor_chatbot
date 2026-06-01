from pathlib import Path
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise ValueError("파일이 존재하지 않습니다.")

    if path.suffix.lower() != ".pdf":
        raise ValueError("pdf 파일만 지원합니다.")

    reader = PdfReader(str(path))
    texts = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            texts.append(page_text)

    content = "\n".join(texts).strip()

    if not content:
        raise ValueError("PDF에서 추출된 텍스트가 없습니다.")

    return content

def extract_text_from_file(file_path: str) -> str:
    return extract_text_from_pdf(file_path)