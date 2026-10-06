"""Embed questions.csv into tracker/template.html.

Writes tracker/index.html (the claude.ai artifact, which saves progress to the
artifact's database) and, with --site DIR, a standalone website in DIR that saves
each visitor's progress in their own browser, with the PDFs copied to DIR/pdf/.
"""
import csv, glob, json, os, shutil, sys

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
    head = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    page = head + page.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n"
    open(os.path.join(site, "index.html"), "w").write(page)
    for pdf in glob.glob("PSAT_Math_Part*.pdf"):
        shutil.copy(pdf, os.path.join(site, "pdf", pdf))
    print(f"Wrote website to {site}/")
