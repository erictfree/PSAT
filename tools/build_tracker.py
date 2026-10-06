"""Embed questions.csv into tracker/template.html, writing tracker/index.html."""
import csv, json

rows = list(csv.DictReader(open("questions.csv")))
domains = sorted({r["domain"] for r in rows})
pairs = sorted({(r["domain"], r["skill"]) for r in rows})
skills = [s for _, s in pairs]
data = {
    "domains": domains,
    "skills": [[domains.index(d), s] for d, s in pairs],
    "q": [[int(r["n"]), r["id"], skills.index(r["skill"]), "EMH".index(r["difficulty"][0]),
           r["answer"], int(r["part"]), int(r["page"])] for r in rows],
}
blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
html = open("tracker/template.html").read().replace("__DATA__", blob)
open("tracker/index.html", "w").write(html)
print(f"Wrote tracker/index.html ({len(rows)} questions)")
