import base64, shutil, pathlib

src_dir = pathlib.Path(r'C:\Users\shree\.gemini\antigravity-ide\brain\e45c8542-538d-44e7-9b8f-32b46e0662c7')
dst_dir = pathlib.Path(r'C:\Users\shree\Desktop\New Blackhole Programs\web')

files = {
    'stellar_bh.png': 'stellar_blackhole_1783497294545.png',
    'supermassive_bh.png': 'supermassive_blackhole_1783497304028.png',
    'intermediate_bh.png': 'intermediate_blackhole_1783497315043.png',
}

for dst_name, src_name in files.items():
    src = src_dir / src_name
    dst = dst_dir / dst_name
    shutil.copy(src, dst)
    print(f"Copied {src_name} -> {dst}")

print("All done.")
