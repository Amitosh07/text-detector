import fitz   # PyMuPDF
import sys

if len(sys.argv) < 3:
    print("Usage: python pdf_search.py <pdf_file> <keyword>")
    sys.exit(1)

pdf_file = sys.argv[1]
keyword = sys.argv[2]

doc = fitz.open(pdf_file)

found = False
all_text = ""
for page_num in range(len(doc)):
    text = doc[page_num].get_text()
    all_text += text + "\n"
    lines = text.split("\n")

    for line in lines:
        if keyword.lower() in line.lower():
            print(f"Page {page_num + 1}: {line.strip()}")
            found = True
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(all_text)

if not found:
    print("No matches found.")
