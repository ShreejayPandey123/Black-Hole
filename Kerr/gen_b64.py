import base64, pathlib, sys

base_dir = pathlib.Path(r'C:\Users\shree\.gemini\antigravity-ide\brain\e45c8542-538d-44e7-9b8f-32b46e0662c7')
files = {
    'STELLAR': base_dir / 'stellar_blackhole_1783497294545.png',
    'SUPERMASSIVE': base_dir / 'supermassive_blackhole_1783497304028.png',
    'INTERMEDIATE': base_dir / 'intermediate_blackhole_1783497315043.png',
}

for key, path in files.items():
    data = base64.b64encode(path.read_bytes()).decode()
    uri = f"data:image/png;base64,{data}"
    out_path = base_dir / f'{key.lower()}_b64.txt'
    out_path.write_text(uri)
    print(f"{key}: written {len(uri)} chars to {out_path.name}")
