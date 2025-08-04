#!/usr/bin/env python3
import re, requests
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract


def extract_pdf_text(file_path):
    try:
        return extract_text(file_path).strip()
    except Exception:
        print("[!] PDF parse failed, using OCR.")
        text = ""
        for img in convert_from_path(file_path, dpi=300):
            text += pytesseract.image_to_string(img)
        return text.strip()


def guess_name_from_url(url):
    parsed = urlparse(url)
    if not parsed.netloc:
        return None
    match = re.search(r"/([^/]+)/\d{4}/\d{2}/", parsed.path)
    if match:
        return match.group(1)
    match = re.search(r"([^/]+)\.pdf", parsed.path, re.IGNORECASE)
    if match:
        return match.group(1).split("+")[0]
    return None


def fallback_name_from_text(text):
    match = re.search(r"(www\.[\w\-\.]+\.\w+)", text)
    if match:
        return match.group(1).replace("www.", "").replace(".", "_")
    return datetime.now().strftime("document_%Y%m%d_%H%M%S")


def main():
    url = input("Enter a PDF URL:\n> ").strip()
    if not url.lower().endswith(".pdf"):
        print("That doesn't look like a PDF URL.")
        return

    tmp_pdf = Path("tmp_download.pdf")
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(tmp_pdf, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    except Exception as e:
        print(f"[!] Failed to download PDF: {e}")
        return

    print("[*] Extracting text...")
    text = extract_pdf_text(tmp_pdf)
    tmp_pdf.unlink()

    name = guess_name_from_url(url) or fallback_name_from_text(text)
    name = re.sub(r"[^\w\-]+", "_", name)

    save_path = Path("rawText")
    save_path.mkdir(exist_ok=True)
    out_file = save_path / f"{name}.txt"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"[+] Saved to {out_file.resolve()}")


if __name__ == "__main__":
    main()
