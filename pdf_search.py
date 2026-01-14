import fitz  # PyMuPDF
import sys
from rapidfuzz import fuzz

# ---------------- CONFIG ----------------
FUZZY_THRESHOLD = 80   # 0–100 (higher = stricter)
# ----------------------------------------

# Check arguments
if len(sys.argv) < 3:
    print("Usage: python pdf_search.py <pdf_file> <keyword>")
    sys.exit(1)
    
pdf_file = sys.argv[1]
keyword = sys.argv[2].lower()

# Open PDF
doc = fitz.open(pdf_file)

found = False
count = 0

# Clear old output file
open("output.txt", "w", encoding="utf-8").close()

print("\nSearching for (fuzzy):", keyword)
print("-" * 50)

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    lines = text.split("\n")

    for line in lines:
        words = line.split()

        matched = False
        best_word = ""
        best_score = 0

        for word in words:
            score = fuzz.partial_ratio(keyword, word.lower())

            if score > best_score:
                best_score = score
                best_word = word

            if score >= FUZZY_THRESHOLD:
                matched = True
                break

        if matched:
            print(f"Page {page_num + 1}: {line.strip()}")
            print(f"   ↳ matched word: '{best_word}'  similarity: {best_score}%\n")

            with open("output.txt", "a", encoding="utf-8") as f:
                f.write(f"Page {page_num + 1}: {line.strip()}\n")

            found = True
            count += 1

            # Highlight approximate word in PDF
            try:
                areas = page.search_for(best_word, flags=fitz.TEXT_IGNORECASE)
                for area in areas:
                    page.add_highlight_annot(area)
            except:
                pass

# Save highlighted PDF
doc.save("highlighted.pdf")
doc.close()

# Final result
if not found:
    print("\nNo fuzzy matches found.")
else:
    print("\nTotal fuzzy matches:", count)
    print("Results saved in output.txt")
    print("Highlighted PDF saved as highlighted.pdf")
