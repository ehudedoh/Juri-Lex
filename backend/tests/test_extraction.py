import io
import shutil

import pytest

from app import extraction


def _tesseract_available() -> bool:
    return shutil.which("tesseract") is not None


def make_docx_bytes(paragraphs):
    import docx

    d = docx.Document()
    for p in paragraphs:
        d.add_paragraph(p)
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


def make_pdf_bytes():
    from pypdf import PdfWriter

    w = PdfWriter()
    w.add_blank_page(width=200, height=200)
    buf = io.BytesIO()
    w.write(buf)
    return buf.getvalue()


def make_image_bytes(text="BONJOUR"):
    from PIL import Image, ImageDraw

    im = Image.new("RGB", (500, 220), "white")
    draw = ImageDraw.Draw(im)
    try:
        from PIL import ImageFont

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
    except Exception:
        font = None
    draw.text((40, 70), text, fill="black", font=font)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def test_detect_type_pdf():
    assert extraction.detect_type(b"%PDF-1.4 fake") == "pdf"


def test_detect_type_docx():
    assert extraction.detect_type(make_docx_bytes(["bonjour"])) == "docx"


def test_detect_type_image():
    assert extraction.detect_type(make_image_bytes()) == "image"


def test_detect_type_unknown():
    assert extraction.detect_type(b"hello world") is None


def test_extract_docx(tmp_path):
    path = tmp_path / "doc.bin"
    path.write_bytes(make_docx_bytes(["Premier paragraphe", "Second paragraphe"]))
    result = extraction.extract_docx(str(path))
    assert result.method == "docx_text"
    assert "Premier paragraphe" in result.text
    assert "Second paragraphe" in result.text


def test_extract_pdf_blank(tmp_path):
    path = tmp_path / "doc.bin"
    path.write_bytes(make_pdf_bytes())
    result = extraction.extract_pdf(str(path), session_dir=None)
    assert result.page_count == 1
    assert result.method == "ocr"
    assert "Page(s) sans texte" in result.warnings[0]


@pytest.mark.skipif(not _tesseract_available(), reason="tesseract indisponible")
def test_ocr_image(tmp_path):
    path = tmp_path / "img.png"
    path.write_bytes(make_image_bytes("BONJOUR"))
    text = extraction.ocr_image(str(path))
    assert "bonjour" in text.lower().replace(" ", "")
