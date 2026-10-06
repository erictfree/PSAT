"""Embed questions.csv into tracker/template.html.

Writes tracker/index.html (the claude.ai artifact, which saves progress to the
artifact's database) and, with --site DIR, an offline folder: open DIR/index.html straight from disk.
It saves progress in that browser, and carries each PDF as DIR/pdf/partN.js
because pages opened from disk can't fetch neighbouring files.
"""
import base64, csv, glob, json, os, shutil, sys

README_TXT = """PSAT Math Question Bank — offline tracker

Open index.html in Chrome, Edge, Firefox or Safari (double-click it).
No internet connection or install is needed.

- If a question says part3.js or part4.js is missing, copy those files into the
  pdf folder here (they come in a second download).
- Click "Show question" on any row to see it; "Show solution" shows the answer and explanation.
- Mark each question correct, missed, or flagged. Add notes if you like.
- Progress is saved in the browser you use, on this computer. Keep this folder in
  the same place and use the same browser, or your marks won't show up.
"""

rows = list(csv.DictReader(open("questions.csv")))
domains = sorted({r["domain"] for r in rows})
pairs = sorted({(r["domain"], r["skill"]) for r in rows})
skills = [s for _, s in pairs]
data = {
    "domains": domains,
    "skills": [[domains.index(d), s] for d, s in pairs],
    "q": [[int(r["n"]), r["id"], skills.index(r["skill"]), "EMH".index(r["difficulty"][0]),
           r["answer"], int(r["part"]), int(r["page"]), float(r["q_y"]),
           int(r["ans_page"]), float(r["ans_y"]), int(r["end_page"]), float(r["end_y"])] for r in rows],
}
blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
template = open("tracker/template.html").read().replace("__DATA__", blob)
open("tracker/index.html", "w").write(template.replace("__STORE__", "claude"))
print(f"Wrote tracker/index.html ({len(rows)} questions)")

if "--site" in sys.argv:
    site = sys.argv[sys.argv.index("--site") + 1]
    os.makedirs(os.path.join(site, "pdf"), exist_ok=True)
    page = template.replace("__STORE__", "local")
    # Use the bundled pdf.js so the folder works with no internet connection.
    os.makedirs(os.path.join(site, "lib"), exist_ok=True)
    for js in ["pdf.min.js", "pdf.worker.min.js"]:
        shutil.copy(os.path.join("tracker", "vendor", js), os.path.join(site, "lib", js))
    page = page.replace("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/", "lib/")
    head = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    page = head + page.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n"
    open(os.path.join(site, "index.html"), "w").write(page)
    for part in [1, 2, 3, 4]:
        pdf = glob.glob(f"PSAT_Math_Part{part}_*.pdf")[0]
        b64 = base64.b64encode(open(pdf, "rb").read()).decode()
        with open(os.path.join(site, "pdf", f"part{part}.js"), "w") as f:
            f.write(f'(window.PSAT_PDF = window.PSAT_PDF || {{}})[{part}] = "{b64}";\n')
    with open(os.path.join(site, "README.txt"), "w") as f:
        f.write(README_TXT)
    print(f"Wrote offline folder to {site}/")
