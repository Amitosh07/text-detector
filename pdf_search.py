import fitz   # PyMuPDF
import sys

# Check arguments
if len(sys.argv) < 3:
    print("Usage: python pdf_search.py <pdf_file> <keyword>")
    sys.exit(1)

pdf_file = sys.argv[1]
keyword = sys.argv[2]

# Open PDF
doc = fitz.open(pdf_file)

found = False
count = 0

# Clear old output file
open("output.txt", "w", encoding="utf-8").close()

print("\nSearching for:", keyword)
print("-" * 40)

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    lines = text.split("\n")

    # Search and print matching lines
    for line in lines:
        if keyword.lower() in line.lower():
            print(f"Page {page_num + 1}: {line.strip()}")
            found = True
            count += 1

            with open("output.txt", "a", encoding="utf-8") as f:
                f.write(f"Page {page_num + 1}: {line.strip()}\n")

    # Highlight keyword in PDF
    text_instances = page.search_for(keyword, flags=fitz.TEXT_IGNORECASE)
    for inst in text_instances:
        page.add_highlight_annot(inst)

# Save highlighted PDF
doc.save("highlighted.pdf")

if not found:
    print("\nNo matches found.")
else:
    print("\nTotal matches:", count)
    print("Results saved in output.txt")
    print("Highlighted PDF saved as highlighted.pdf")

doc.close()
