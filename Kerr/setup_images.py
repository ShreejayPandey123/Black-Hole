"""
Run this script once to copy the black hole images to the web folder.
Usage: python setup_images.py
"""
import shutil
import pathlib
import sys

src = pathlib.Path(r'C:\Users\shree\.gemini\antigravity-ide\brain\e45c8542-538d-44e7-9b8f-32b46e0662c7')
dst = pathlib.Path(r'C:\Users\shree\Desktop\New Blackhole Programs\web')

copies = [
    ('stellar_blackhole_1783497294545.png', 'stellar_bh.png'),
    ('supermassive_blackhole_1783497304028.png', 'supermassive_bh.png'),
    ('intermediate_blackhole_1783497315043.png', 'intermediate_bh.png'),
]

all_ok = True
for src_name, dst_name in copies:
    s = src / src_name
    d = dst / dst_name
    if not s.exists():
        print(f"ERROR: Source not found: {s}")
        all_ok = False
        continue
    shutil.copy(s, d)
    print(f"Copied: {dst_name} ({d.stat().st_size:,} bytes)")

if all_ok:
    print("\nAll images copied successfully!")
    print("Open web/index.html in your browser, go to Settings > Guide tab.")
else:
    print("\nSome files were not found. Please check the paths.")
    sys.exit(1)
