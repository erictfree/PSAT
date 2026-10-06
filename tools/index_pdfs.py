"""Build questions.csv from the four question-bank PDFs.

Needs PyMuPDF (pip install pymupdf). Besides each question's metadata, it records
where the question and its solution sit in the PDF (page numbers and y offsets in
PDF points), which the tracker uses to show them inline.
"""
import csv, glob, re
import pymupdf

FIELDS = ["n", "id", "domain", "skill", "difficulty", "answer", "part", "pdf", "page",
          "q_y", "ans_page", "ans_y", "end_page", "end_y"]


def header_columns(page, top):
    """Domain and skill text from the metadata table under the 'Question ID' title."""
    words = page.get_text("words")
    labels = {w[4]: w for w in words if top < w[1] < top + 60 and w[4] in ("Domain", "Skill", "Difficulty")}
    cd, cs, cf = labels["Domain"][0], labels["Skill"][0], labels["Difficulty"][0]
    row_top = labels["Domain"][3] + 5
    body = [w for w in words if row_top < w[1] < row_top + 70]
    pick = lambda x0, x1: " ".join(w[4] for w in sorted(body, key=lambda w: (round(w[1]), w[0])) if x0 - 3 <= w[0] < x1 - 3)
    return pick(cd, cs), pick(cs, cf)


rows = []
for part in [1, 2, 3, 4]:
    pdf = glob.glob(f"PSAT_Math_Part{part}_*.pdf")[0]
    cur = None
    for pn, page in enumerate(pymupdf.open(pdf), 1):
        for b in sorted(page.get_text("blocks"), key=lambda b: b[1]):
            t = b[4].strip()
            if m := re.match(r"Question ID ([0-9a-f]+)$", t):
                domain, skill = header_columns(page, b[1])
                cur = dict(n=len(rows) + 1, id=m.group(1), domain=domain, skill=skill,
                           answer="", difficulty="", part=part, pdf=pdf, page=pn)
                rows.append(cur)
            elif not cur:
                continue
            elif re.match(r"ID: [0-9a-f]+ Answer$", t):
                cur["ans_page"], cur["ans_y"] = pn, round(b[1] - 12, 1)  # clears the dark "Answer" header bar
            elif re.match(r"ID: [0-9a-f]+$", t) and "q_y" not in cur:
                cur["q_y"] = round(b[3] + 10, 1)  # clears the underline below the ID label
            elif m := re.match(r"Correct Answer:\s*(.*)", t):
                cur["answer"] = cur["answer"] or m.group(1).strip()
            elif m := re.match(r"Question Difficulty:\s*(\w+)", t):
                cur["difficulty"] = cur["difficulty"] or m.group(1)
                cur["end_page"], cur["end_y"] = pn, round(b[3] + 6, 1)

missing = [r["n"] for r in rows if any(k not in r for k in FIELDS)]
assert not missing, f"incomplete rows: {missing[:10]}"
with open("questions.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow({k: r[k] for k in FIELDS})
print(f"Wrote {len(rows)} questions to questions.csv")
