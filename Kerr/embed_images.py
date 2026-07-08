"""
Embeds the three black hole images as base64 data URIs directly into index.html
so they work without any file copying.
Run: python embed_images.py
"""
import base64
import pathlib
import re

src = pathlib.Path(r'C:\Users\shree\.gemini\antigravity-ide\brain\e45c8542-538d-44e7-9b8f-32b46e0662c7')
html_path = pathlib.Path(r'C:\Users\shree\Desktop\New Blackhole Programs\web\index.html')

images = {
    'stellar_bh.png': src / 'stellar_blackhole_1783497294545.png',
    'supermassive_bh.png': src / 'supermassive_blackhole_1783497304028.png',
    'intermediate_bh.png': src / 'intermediate_blackhole_1783497315043.png',
}

html = html_path.read_text(encoding='utf-8')

for fname, fpath in images.items():
    if not fpath.exists():
        print(f"SKIP (not found): {fpath}")
        continue
    b64 = base64.b64encode(fpath.read_bytes()).decode()
    data_uri = f"data:image/png;base64,{b64}"
    old = f'src="{fname}"'
    new = f'src="{data_uri}"'
    if old in html:
        html = html.replace(old, new)
        print(f"Embedded: {fname} ({len(b64):,} chars)")
    else:
        print(f"WARNING: '{old}' not found in HTML")

html_path.write_text(html, encoding='utf-8')
print(f"\nDone! Patched: {html_path}")
print("Open web/index.html → Settings → Guide tab to see the infographic.")
