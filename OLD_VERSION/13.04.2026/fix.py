import os

files = [
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\index.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\b2b.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\cert.html',
]

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()

        # 1. Update Fonts to Inter
        text = text.replace('family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Noto+Sans:wght@300;400;500;700', 'family=Inter:wght@300;400;500;600;700')
        text = text.replace('family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&family=Noto+Sans:wght@300;400;700', 'family=Inter:wght@300;400;500;600;700')

        text = text.replace('\'Lora\', serif', '\'Inter\', -apple-system, sans-serif')
        text = text.replace('\'Lora\', Georgia, \'Times New Roman\', serif', '\'Inter\', -apple-system, sans-serif')
        text = text.replace('\'Noto Sans\', sans-serif', '\'Inter\', -apple-system, sans-serif')
        text = text.replace('\'Playfair Display\', serif', '\'Inter\', -apple-system, sans-serif')

        # 2. Fix titles and descriptions
        text = text.replace('Klinik Psixoloq, Həkim Psixoterapevt', 'Həkim-psixiatr, Psixoterapevt')
        text = text.replace('Həkim Psixoterapevt, Klinik Psixoloq', 'Həkim-psixiatr, Psixoterapevt')
        text = text.replace('Həkim psixoterapevt, klinik psixoloq', 'Həkim-psixiatr, psixoterapevt')
        
        # 3. Fix Karvasarski
        text = text.replace('B.D.Karvasarski tərəfindən hazırlanmışdır', 'professor B.D.Karvasarskinin rəhbərliyi altında təhsil almışdır')
        text = text.replace('B.D.Karvasarski tərəfindən hazırlanmış', 'professor B.D.Karvasarskinin rəhbərliyi altında təhsil almış')
        text = text.replace('bilavasitə hazırlanmış', 'təhsil almışdır')

        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Updated {file}")
    except Exception as e:
        print(f"Skipping {file} due to error or missing: {e}")
