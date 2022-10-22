import os, errno, shutil
import json
import  requests 
import  tarfile
import tqdm

from glob2 import glob

from unicode_hell import doubledecode

DATA = 'https://mystic.the-eye.eu/public/AI/training_data/wikiart/Wikiart-with-captions-tar/wikiart1.tar'
STRING = '''\\'''
DIR = 'temp'
OUTPUT = 'dataset.json'
def make_dir(dir):
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def delete_tree(dir):
    try:
        shutil.rmtree(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def get_file(link):
    make_dir(DIR)
    with requests.get(link, stream=True) as rx, tarfile.open(fileobj=rx.raw, mode='r|*') as tarobj: 
        tarobj.extractall(DIR)
    
def read_files():
    images = glob(f'{DIR}/**/*.jpg', recursive=True)
    texts = [img.replace('jpg', 'txt') for img in images]
    results = []
    
    for img, txt in tqdm.tqdm(zip(images, texts), leave=False):
        with open(txt, 'r', encoding='utf-8') as f:
            line = f.read()
            line = doubledecode(line.encode('utf-8', errors='ignore'))
        
        results.append({'image': f'/content/{img.replace(STRING, "/")}',
                        'text': line})
    
    return results

def main(n=1, delete=True):
    results = []
    
    for i in tqdm.tqdm(range(1, n+1)):
        if delete: delete_tree(DIR)
            
        get_file(DATA.replace('1', str(i)))
        
        results.append({f'wikiart{i}': read_files()})
        
        with open(OUTPUT, 'w') as f:
            json.dump(results, f, ensure_ascii=True, indent=1)
        
    if delete: delete_tree(DIR)

if __name__ == '__main__':
    main(5)