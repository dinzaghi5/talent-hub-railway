import sys
import fitz

doc = fitz.open('D:/PROJECT/CODE/TALEND_HUB/BE/KOL_AZZURA_TASYA_2005_127.pdf')
page = doc[0]

with open('pdf_debug.txt', 'w', encoding='utf-8') as f:
    text_instances = page.get_text('dict')['blocks']
    f.write('--- PDF Text Content and Basic Positioning ---\n')
    for block in text_instances:
        if block.get('type') == 0:
            for line in block['lines']:
                for span in line['spans']:
                    text_content = span['text'].strip()
                    if not text_content: continue
                    bbox = [round(x, 1) for x in span['bbox']]
                    if isinstance(span['color'], int):
                        h = hex(span['color'])[2:]
                        h = '0' * (6 - len(h)) + h
                    else:
                        h = str(span['color'])
                    f.write(f"Text: {repr(text_content)} | Font: {span['font']} | Size: {round(span['size'], 1)} | Color: {h} | BBox: {bbox}\n")

    f.write('\n--- PDF Drawings ---\n')
    paths = page.get_drawings()
    for p in paths:
        bbox = [round(x, 1) for x in p['rect']]
        fill = str(p.get('fill'))
        color = str(p.get('color'))
        width = round(p.get('width', 0) or 0, 1)
        f.write(f"Fill Color: {fill} | Stroke Color: {color} | Width: {width} | Rect: {bbox}\n")

print('Done')
