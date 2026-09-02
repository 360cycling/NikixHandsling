"""Build a self-contained index.html from index.src.html by embedding every
image/favicon as a data URI. Edit index.src.html, then run: python build_standalone.py"""
import base64, os, re
root = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(root, "index.src.html"), encoding="utf-8").read()

def datauri(path, mime):
    b = open(os.path.join(root, path), "rb").read()
    return "data:%s;base64,%s" % (mime, base64.b64encode(b).decode())

media = {
    "assets/img/hero-win.jpg": "image/jpeg",
    "assets/img/race-scene.jpg": "image/jpeg",
    "assets/img/win-celebration.jpg": "image/jpeg",
    "assets/img/peloton.jpg": "image/jpeg",
    "assets/img/favicon.svg": "image/svg+xml",
}
for path, mime in media.items():
    if path not in html:
        print("note: not referenced, skipping", path)
        continue
    html = html.replace(path, datauri(path, mime))

open(os.path.join(root, "index.plain.html"), "w", encoding="utf-8").write(html)
left = re.findall(r"assets/[^\"')]+", html)
print("readable build index.plain.html:", round(len(html.encode("utf-8")) / 1048576, 2), "MB;",
      "remaining assets refs:", set(left) if left else "NONE")
print("Next: python lock.py \"<passphrase>\"  ->  writes the locked index.html for deployment")
