import sys, re
f = sys.argv[1]
text = open(f, encoding="utf-8", errors="ignore").read()
lines = text.split("\n")
page = 1
res = []
for ln in lines:
    if "\f" in ln:
        page += 1
    res.append((page, ln))
pats = sys.argv[2:]
for p in pats:
    print("### pattern:", p)
    cnt=0
    for pg, ln in res:
        if re.search(p, ln, re.I) and len(ln.strip())>0:
            print(f"  p.{pg:>2} | {ln.strip()[:90]}")
            cnt+=1
            if cnt>=6: break
