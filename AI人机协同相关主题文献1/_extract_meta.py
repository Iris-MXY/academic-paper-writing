import fitz, os, json, re

root = r"C:\Users\tianb\Desktop\AI相关论文\AI人机协同相关主题文献"
out = []
files = [f for f in os.listdir(root) if f.lower().endswith(".pdf")]
files.sort()

def clean(s):
    return re.sub(r"[\s\u200b]+", " ", s).strip()

for fn in files:
    path = os.path.join(root, fn)
    try:
        doc = fitz.open(path)
    except Exception as e:
        out.append({"file": fn, "error": str(e)})
        continue
    n = doc.page_count
    full = "".join(doc[i].get_text() for i in range(n))
    # title
    title = ""
    head = doc[0].get_text()
    for ln in head.splitlines():
        ln = clean(ln)
        if len(ln) > 10 and "downloaded by" not in ln.lower() and "preprint" not in ln.lower():
            title = ln; break
    if not title:
        title = fn
    # abstract
    abstract = ""
    m = re.search(r"Abstract[\s\:\.\-]*\n?(.*?)(?:Keywords|JEL|1\.\s*Introduction|Introduction|DOI|Copyright)", full, re.I|re.S)
    if m:
        abstract = clean(m.group(1))
    else:
        # grab first 800 chars after title area
        abstract = clean(full[:2500])
    # section-based snippets
    snippets = {}
    for i in range(n):
        txt = doc[i].get_text()
        for ln in txt.splitlines():
            l = clean(ln)
            if re.match(r"^\s*(\d+\.|\d+\.\d+)\s+[A-Z]", l) and len(l) < 75:
                key = l.lower()
                if any(k in key for k in ["method","experiment","empirical","data","model","theor","framework","result","finding","conclusion","discussion","design","setup","procedure"]):
                    snippets[key] = clean(txt)[:1500]
    last = clean(doc[max(0,n-1)].get_text())[:1500]
    out.append({
        "file": fn, "title": title, "pages": n,
        "abstract": abstract[:1500],
        "snippets": snippets, "last_page": last,
    })
    doc.close()

with open(os.path.join(root, "_meta.json"), "w",  encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# quick dump readable
with open(os.path.join(root, "_abstracts.txt"), "w", encoding="utf-8") as f:
    for o in out:
        f.write(f"\n===== {o['file']} (p{o.get('pages')}) =====\n")
        f.write("TITLE: " + o.get('title','') + "\n")
        f.write("ABS: " + o.get('abstract','')[:900] + "\n")
print("done", len(out))
