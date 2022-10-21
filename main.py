import os
import json

from glob2 import glob

from unicode_hell import doubledecode

DATA = 'wikiart-with-captions'
STRING = '''\\'''

def main():
    images = glob(f'{DATA}/*.jpg', recursive=True)
    texts = [img.replace('jpg', 'txt') for img in images]
    
    lines = []
    for img, txt in zip(images, texts):
        with open(txt, 'r', encoding='utf-8') as f:
            line = f.read()
            line = doubledecode(line.encode('utf-8', errors='ignore'))
        
        lines.append({'image': f'/content/{img.replace(STRING, "/")}',
                      'text': line})
        
    with open('dataset.json', 'w') as f:
        json.dump(lines, f, ensure_ascii=True, indent=1)
        
    

if __name__ == '__main__':
    main()