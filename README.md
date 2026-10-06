# PSAT

PSAT/NMSQT & PSAT 10 Math question bank: 1,366 questions split across four PDFs.

| File | Questions |
| --- | --- |
| `PSAT_Math_Part1_q1-350.pdf` | 1–350 |
| `PSAT_Math_Part2_q351-700.pdf` | 351–700 |
| `PSAT_Math_Part3_q701-1050.pdf` | 701–1050 |
| `PSAT_Math_Part4_q1051-1366.pdf` | 1051–1366 |

## Question index

`questions.csv` lists every question: running number, College Board question ID,
domain, skill, difficulty, correct answer, and the PDF and page it starts on.

| Domain | Questions |
| --- | --- |
| Algebra | 484 |
| Advanced Math | 387 |
| Problem-Solving and Data Analysis | 273 |
| Geometry and Trigonometry | 222 |

Difficulty: 352 Easy, 448 Medium, 566 Hard. Question ID `af691219` appears twice
(#756 and #776).

## Progress tracker

`tracker/index.html` is a page for marking each question correct, missed, or
flagged for review, with filters by domain, skill, difficulty and status. It is
published as a claude.ai artifact and saves progress there.

## Regenerating

```sh
python3 tools/index_pdfs.py     # PDFs -> questions.csv (needs poppler's pdftotext)
python3 tools/build_tracker.py  # questions.csv + tracker/template.html -> tracker/index.html
```
