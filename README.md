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
`q_y`, `ans_page`/`ans_y` and `end_page`/`end_y` mark where the question and its
solution sit on the page (PDF points from the top), which the tracker uses to crop them.

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
flagged for review, with filters by domain, skill, difficulty and status. Each
question and its solution can be opened inline: the page renders that region of
the source PDF with pdf.js. It is published as a claude.ai artifact, with the four
PDFs alongside it under `pdf/`, and saves progress there.

## Download

**[Download PSAT-Tracker.zip](https://github.com/erictfree/PSAT/raw/claude/cool-dirac-0uv0z2/download/PSAT-Tracker.zip)**
(about 37 MB). Unzip it, then double-click `PSAT-Tracker/index.html`. No account,
install or internet connection needed; progress saves in that browser.

## Offline folder

`python3 tools/build_tracker.py --site _site` builds a folder that works from disk
with no internet: double-click `_site/index.html`. It bundles pdf.js
(`tracker/vendor/`) and carries each PDF as `pdf/partN.js`, because a page opened
from disk can't fetch the files next to it. Progress is saved in that browser.

## Regenerating

```sh
python3 tools/index_pdfs.py     # PDFs -> questions.csv (needs PyMuPDF: pip install pymupdf)
python3 tools/build_tracker.py  # questions.csv + tracker/template.html -> tracker/index.html
python3 tools/build_tracker.py --site _site  # also build the offline folder into _site/
```
