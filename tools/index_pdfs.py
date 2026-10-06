"""Build questions.csv from the four question-bank PDFs (needs poppler's pdftotext)."""
import csv, glob, re, subprocess

FIELDS = ["n", "id", "domain", "skill", "difficulty", "answer", "part", "pdf", "page"]

rows = []
for part in [1, 2, 3, 4]:
    pdf = glob.glob(f"PSAT_Math_Part{part}_*.pdf")[0]
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    cur = None
    for page, pg in enumerate(text.split("\f"), 1):
        lines = pg.split("\n")
        for i, line in enumerate(lines):
            m = re.search(r"Question ID ([0-9a-f]+)", line)
            if m:
                # Header row gives column positions for Domain / Skill / Difficulty.
                hdr = next(j for j in range(i + 1, i + 4) if "Domain" in lines[j])
                h = lines[hdr]
                cd, cs, cf = h.index("Domain"), h.index("Skill"), h.index("Difficulty")
                dom, sk = [], []
                for k in range(hdr + 1, len(lines)):
                    if "ID:" in lines[k]:
                        break
                    dom.append(lines[k][cd - 3:cs - 3].strip())
                    sk.append(lines[k][cs - 3:cf - 3].strip())
                cur = dict(n=len(rows) + 1, id=m.group(1), part=part, pdf=pdf, page=page,
                           domain=" ".join(filter(None, dom)), skill=" ".join(filter(None, sk)),
                           answer="", difficulty="")
                rows.append(cur)
            m = re.search(r"Correct Answer:\s*(.*)", line)
            if m and cur and not cur["answer"]:
                cur["answer"] = m.group(1).strip()
            m = re.search(r"Question Difficulty:\s*(\w+)", line)
            if m and cur and not cur["difficulty"]:
                cur["difficulty"] = m.group(1)

with open("questions.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow({k: r[k] for k in FIELDS})
print(f"Wrote {len(rows)} questions to questions.csv")
