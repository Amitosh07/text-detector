import fitz   # PyMuPDF
import sys

if len(sys.argv) < 3:
    print("Usage: python pdf_search.py <pdf_file> <keyword>")
    sys.exit(1)

pdf_file = sys.argv[1]
keyword = sys.argv[2]

doc = fitz.open(pdf_file)

found = False

for page_num in range(len(doc)):
    text = doc[page_num].get_text()

    if keyword.lower() in text.lower():
        print(f"Found '{keyword}' on page {page_num + 1}")
        found = True

if not found:
    print("No matches found.")
